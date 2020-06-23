
---
title: "Bahamut_websocket.md"
date: 2020-03-17 18:47:27 +0800
lastmod: 2020-06-15 09:12:32 +0800
draft: true
tags: [""]
categories: [""]
author: "Claymore"

---

---
title: "Bahamut_websocket.md"
date: 2020-03-17 18:47:27 +0800
lastmod: 2020-03-17 18:47:27 +0800
draft: true
tags: [""]
categories: [""]
author: "Claymore"

---
## Bahamut_websocket

核心语句：

``` go 
pubSunClient := bahamut.NewLocalPubSubClient()
pubSunClient.Connect()  //.Wait(3 * time.Second)

opts := []bahamut.Option{
		bahamut.OptRestServer(":12345"),
		
  	bahamut.OptPushServer(pubSunClient, "testTopic"),
		bahamut.OptPushDispatchHandler(&handler.MockSessionHandler{}),
		bahamut.OptPushPublishHandler(&handler.MockSessionHandler{}),

}
server := bahamut.New(opts...)
server.Run(context.Background())
```

关于 OptRestServer 的启动 在  『ApiServer 启动流程记录』里面说过， 这里记录下 OptPushServer 的启动



### PubSubClient

`bahamut.NewLocalPubSubClient() `-> bahamut/pubsub_local.go：

``` go
// localPubSub implements a PubSubClient using local channels
type localPubSub struct {
	subscribers  map[string][]chan *Publication
	register     chan *registration
	unregister   chan *registration
	publications chan *Publication
	stop         chan struct{}

	lock *sync.Mutex
}

// NewLocalPubSubClient returns a PubSubClient backed by local channels.
func NewLocalPubSubClient() PubSubClient {
	return newlocalPubSub()
}

// newlocalPubSub returns a new localPubSub.
func newlocalPubSub() *localPubSub {

	return &localPubSub{
		subscribers:  map[string][]chan *Publication{},
		register:     make(chan *registration), 
		unregister:   make(chan *registration),
		stop:         make(chan struct{}),
		publications: make(chan *Publication, 1024),
		lock:         &sync.Mutex{},
	}
}
```

这里全是声明的 channel, channel 类型 为Pulcation 涉及到的 Publication 结构体：

``` go
type Publication struct {
	Data         []byte                     `msgpack:"data,omitempty" json:"data,omitempty"`
	Topic        string                     `msgpack:"topic,omitempty" json:"topic,omitempty"`
	Partition    int32                      `msgpack:"partition,omitempty" json:"partition,omitempty"`
	TrackingName string                     `msgpack:"trackingName,omitempty" json:"trackingName,omitempty"`
	TrackingData opentracing.TextMapCarrier `msgpack:"trackingData,omitempty" json:"trackingData,omitempty"`
	Encoding     elemental.EncodingType     `msgpack:"encoding,omitempty" json:"encoding,omitempty"`
	ResponseMode ResponseMode               `msgpack:"responseMode,omitempty" json:"responseMode,omitempty"`

	replyCh  chan *Publication
	replied  bool
	timedOut bool
	mux      sync.Mutex
	span     opentracing.Span
}
```

涉及到的 registration 结构体

``` go 
type registration struct {
	topic string  // 主题, 注意上方 Publication 里也有个 Topic
	ch    chan *Publication
}
```

如果把 channel 想象成 channel， 那么 Publication 和 registration 则为 channel 中的结构体。



#### connect

``` go
// Connect connects the PubSubClient to the remote service.
func (p *localPubSub) Connect() Waiter {

	abort := make(chan struct{})
	connected := make(chan bool)

	go func() {
		go p.listen()  // 监听
		connected <- true
	}()

  // 返回了两个channel(并没有使用)， 遗留了 p.listen() 这个 Goroutline 在阻塞。
	return connectionWaiter{
		ok:    connected,
		abort: abort,
	}
}
```



#### listen

``` go
func (p *localPubSub) listen() {
	for {
		select {
    // 如果 register channel（注册管道) 有值可读
		case reg := <-p.register:
			p.lock.Lock()  // 锁
			if _, ok := p.subscribers[reg.topic]; !ok {
				p.subscribers[reg.topic] = []chan *Publication{} // 用 map 存储起来。
			}

      // 把某个主题的registration 的 Publication 在 subscribers 里赋值。
			p.subscribers[reg.topic] = append(p.subscribers[reg.topic], reg.ch)
			p.lock.Unlock() // 解锁

		case reg := <-p.unregister:  // 取消注册
			p.lock.Lock()
			for i, sub := range p.subscribers[reg.topic] {
				if sub == reg.ch {
					p.subscribers[reg.topic] = append(p.subscribers[reg.topic][:i], p.subscribers[reg.topic][i+1:]...)
					close(sub)  // 关闭cannel
					break
				}
			}
			p.lock.Unlock()

    // 
		case publication := <-p.publications:
			p.lock.Lock()
			var wg sync.WaitGroup 
      // 这里应该在管道 存入的时候，在subscribers 中 存入的值（主题名: Pulcation channel）
			for _, sub := range p.subscribers[publication.Topic] {
				wg.Add(1)
				go func(s chan *Publication, p *Publication) {
					defer wg.Done() 
					s <- p.Duplicate() // 复制一个 pulication 给 Pulcation channel
				}(sub, publication)
			}
      wg.Wait() // 等待 wg.Done() 将 WatiGroup 减为 0.
			p.lock.Unlock()

		case <-p.stop:
			p.lock.Lock()
			p.subscribers = map[string][]chan *Publication{} //将subscribers 清空。 
			p.lock.Unlock()
			return
		}
	}
}
```



### PushServer

`bahamut.OptPushServer(pubSunClient, "testTopic"),`

在 options.go:

``` go
func OptPushServer(service PubSubClient, topic string) Option {
	return func(c *config) {
		c.pushServer.enabled = true  // 开启
		c.pushServer.service = service 
		c.pushServer.topic = topic
    // config 中的 pushServer 结构：
    // pushServer struct { 
    //   	service PubSubClient
    //    topic   string
    //    ...
	}
}
```



Server := bahamut.New(opts...) -> bahamut.go: NewServer:

``` go
if cfg.pushServer.enabled {
		srv.pushServer = newPushServer(cfg, mux, srv.ProcessorForIdentity)
	}

// websocket_server.go: 
func newPushServer(cfg config, multiplexer *bone.Mux, processorFinder processorFinderFunc) *pushServer {

	srv := &pushServer{
		sessions:        map[string]*wsPushSession{}, // session
		multiplexer:     multiplexer,
		cfg:             cfg,
		sessionsLock:    sync.RWMutex{},
		processorFinder: processorFinder,
		publications:    make(chan *Publication, 24000), // 构造 Pulication chan, 和上方联系起来
    mainContext     context.Context 
	}

	endpoint := cfg.pushServer.endpoint
	if endpoint == "" {
		endpoint = "/events"  // 默认路由路径
	}
  
	// 配置  websocket 路由
	if cfg.pushServer.enabled && cfg.pushServer.dispatchEnabled {
    // srv.handleRequest 是 pushServer 的一个方法，是重点，但是这里方法没有执行。
    // 因为这里 multiplexer 会该将该handle 注册到 get方法中，当你get endpoint的时候才会执行。
    // 具体在下方：
		srv.multiplexer.Get(endpoint, http.HandlerFunc(srv.handleRequest))
		fmt.Println("Websocket push handlers installed")
		zap.L().Debug("Websocket push handlers installed")
	}

	return srv
}
```



#### Run

由 sever.Run(context.Background) 我们看pushServer.start(ctx):

``` go
func (n *pushServer) start(ctx context.Context) {

	n.mainContext = ctx

	if n.cfg.pushServer.service != nil {
		errors := make(chan error, 24000)  // 错误处理 channel
		defer n.cfg.pushServer.service.Subscribe(n.publications, errors, n.cfg.pushServer.topic)()
	}

	for {
		select {
		case p := <-n.publications:  // 如果 pulications 里 有值可读
			go func(publication *Publication) {
				event := &elemental.Event{}
				if err := publication.Decode(event); err != nil {
					// pulication 的解码错误判断
					return
				}

				// 解码出两种格式
				dataMSGPACK, dataJSON, err := prepareEventData(event)
				if err != nil {
				// 错误输出
					return
				}

				// 其实这里是统计 event 次数
				var eventSummary interface{}
				if n.cfg.pushServer.dispatchHandler != nil {
					eventSummary, err = n.cfg.pushServer.dispatchHandler.SummarizeEvent(event)
			  // ..
						return
					}
				}

				// Keep a references to all current ready push sessions as it may change at any time, we lost 8h on this one...
       // 获取所有 sessin
				n.sessionsLock.RLock()
				sessions := make([]*wsPushSession, len(n.sessions))
				var i int
				for _, s := range n.sessions {
					sessions[i] = s
					i++
				}
				n.sessionsLock.RUnlock()

				// Dispatch the event to all sessions, 分发所有 event 到 sessions
				for _, session := range sessions {

					// If event happened before session, we don't send it.
					if event.Timestamp.Before(session.startTime) {
						continue
					}

					// If the event identity (or related identities) are filtered out
					// we don't send it.  这里就是过滤的过程
					if f := session.currentFilter(); f != nil {

						identities := []string{event.Identity}
						if n.cfg.pushServer.dispatchHandler != nil {
							identities = append(identities, n.cfg.pushServer.dispatchHandler.RelatedEventIdentities(event.Identity)...)
						}

						var ok bool
						for _, identity := range identities {
							if !f.IsFilteredOut(identity, event.Type) {
								ok = true
								break
							}
						}

						if !ok {
							continue
						}
					}
					// 分发 的计数
					if n.cfg.pushServer.dispatchHandler != nil {
						ok, err :=  n.cfg.pushServer.dispatchHandler.ShouldDispatch(session, event, eventSummary)
						if err != nil {
						  //
							continue
						}

						if !ok {
							continue
						}
					}

					switch session.encodingWrite {
          // 真正的send
					case elemental.EncodingTypeMSGPACK:
						session.send(dataMSGPACK)
					case elemental.EncodingTypeJSON:
						session.send(dataJSON)
					}
				}
			}(p)  // p 为 Publication

		case <-ctx.Done():
			return
		}
	}
}
```

目前因为什么消息没有，这里会阻塞



#### handleRequest

``` go
func (n *pushServer) handleRequest(w http.ResponseWriter, r *http.Request) {
	upgrader := websocket.Upgrader{
		// 允许跨域
		CheckOrigin: func(r *http.Request) bool { return true },
	}

	r = r.WithContext(n.mainContext)

  // 从 header 中 获取 编码类型 是 msgpack 还是 json
	readEncodingType, writeEncodingType, err := elemental.EncodingFromHeaders(r.Header)

	// "实例化 session"
	session := newWSPushSession(r, n.cfg, n.unregisterSession, readEncodingType, writeEncodingType)
	session.setTLSConnectionState(r.TLS)

  // 获取 ip
	var clientIP string
	if ip := r.Header.Get("X-Forwarded-For"); ip != "" {
		clientIP = ip
	} else if ip := r.Header.Get("X-Real-IP"); ip != "" {
		clientIP = ip
	} else {
		clientIP = r.RemoteAddr
	}
	session.setRemoteAddress(clientIP)

	// 认证session
	if err := n.authSession(session); err != nil {
		writeHTTPResponse(n.cfg.security.CORSOrigin, w, makeErrorResponse(r.Context(), elemental.NewResponse(elemental.NewRequest()), err, nil))
		return
	}

	// 如果有 dispatchHandler， 也调用它的 OnPushSessionInit 实例化它的session
	if err := n.initPushSession(session); err != nil {
		writeHTTPResponse(n.cfg.security.CORSOrigin, w, makeErrorResponse(r.Context(), elemental.NewResponse(elemental.NewRequest()), err, nil))
		return
	}

	// 将普通 http 升级为 websocket
	ws, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		writeHTTPResponse(n.cfg.security.CORSOrigin, w, makeErrorResponse(r.Context(), elemental.NewResponse(elemental.NewRequest()), err, nil))
		return
	}

	// wsc 是封装了 websocket 的库， 建立连接连接
	conn, err := wsc.Accept(r.Context(), ws, wsc.Config{WriteChanSize: 64, ReadChanSize: 16})
	if err != nil {
		writeHTTPResponse(n.cfg.security.CORSOrigin, w, makeErrorResponse(r.Context(), elemental.NewResponse(elemental.NewRequest()), err, nil))
		return
	}

	session.setConn(conn) // conn 赋值 session 的 conn属性，存储刚才的连接

	fmt.Println("注册session")
	n.registerSession(session)

	// 监听建立好连接的websocket 内容
	session.listen()
}
```

