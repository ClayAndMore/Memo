### 流程

#### Server
1. bottle 中通过:
   ```
    server_names = {
    'cgi': CGIServer,
    'flup': FlupFCGIServer,
    'wsgiref': WSGIRefServer,
    'waitress': WaitressServer,
    'cherrypy': CherryPyServer,
    'paste': PasteServer,
    'fapws3': FapwsServer,
    'tornado': TornadoServer,
    'gae': AppEngineServer,
    'twisted': TwistedServer,
    'diesel': DieselServer,
    'meinheld': MeinheldServer,
    'gunicorn': GunicornServer,
    'eventlet': EventletServer,
    'gevent': GeventServer,
    'geventSocketIO':GeventSocketIOServer,
    'rocket': RocketServer,
    'bjoern' : BjoernServer,
    'auto': AutoServer,
    }
    ```
    默认值wsgiref找到 WSGIRefServer
    执行WSGIRefServer.run()  (bottle.run的直接转化)

2. WSGIRefServer run()里规定了FixedHandler类， 通过wsgiref.simple_server的make_server 方法实现了server类的初始化：
    `WSGIServer((host,port),FixedHandler).server_forever()`
    
    host='127.0.0.1', port=8080

3.  WSGIServer --> TCPServer(__init__) --> BaseServer(__init__)
    ```
        self.server_address = (host, port)
        self.RequestHandlerClass = FixedHandler
        self.__is_shut_down = threading.Event()
        self.__shutdown_request = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP

        self.server_bind()
        self.server_activate()
    ```

 4. init过程中用到了server_bind()
    server_bind(): WSGIServer, HTTPServer, TCPServer
    ```
        self.socket.bind(self.server_address)
        self.server_address = self.socket.getsockname() #('127.0.0.1', 8080)
        host, port = self.socket.getsockname()[:2] #('127.0.0.1', 8080)
        self.server_name = socket.getfqdn(host) # 'localhost.localdomain'
        self.server_port = port # 8080

        self.setup_environ():
        env = self.base_environ = {}
        env['SERVER_NAME'] = self.server_name 
        env['GATEWAY_INTERFACE'] = 'CGI/1.1'
        env['SERVER_PORT'] = str(self.server_port)
        env['REMOTE_HOST']=''
        env['CONTENT_LENGTH']=''
        env['SCRIPT_NAME'] = ''
    ```

    初始化完成

5.  WSGIServer.serve_forever()
    
    ```python
        self.__is_shut_down.clear() #threading.Event().clear()
        try:
            while not self.__shutdown_request:
               虑另一个文件描述符 或 连socket去唤醒而不是POLLING, 
    轮询使关闭请求连接的速度变慢 并且 其他时间在浪费CPU。
                r, w, e = _eintr_retry(select.select, [self], [], [],
                                       poll_interval)
                if self in r:
                    self._handle_request_noblock()
        finally:
            self.__shutdown_request = False
            self.__is_shut_down.set() # event.set()

    ```

    threading.Event().clear()

    while j
    注释: 考虑另一个文件描述符 或 连socket去唤醒而不是POLLING, 
    轮询使关闭请求连接的速度变慢 并且 其他时间在浪费CPU。

    `r, w, e = select.select([self], [], [], 0.5)`  0.5秒的轮询.
    等待 r 可读缓冲区有值


#### handle

1.  接上， 缓冲区有值时 _handle_request_noblock():
    ```python
    request, client_address = self.socket.accept()
    # 初始化HandlerClass, 接受一个请求初始一个Handler
    RequestHandlerClass(request, client_address, self)

    # TCPServer
    self.shutdown_request(request):

    request.shutdown(socket.SHUT_WR) # 连接方 阻止发送数据
    request.close() # 释放socket
    ```

2. RequestHandlerClass 的初始化

    FixedHandler(request, client_address, self) - BaseRequestHandler:
    ```python
    self.request = request
    self.client_address = client_address
    self.server = server   # 即上方的server(self)
    self.connection = self.request
    self.rfile = self.connection.makefile('rb', self.rbufsize) # rbufsize: -1, 全缓冲
    self.wfile = self.connection.makefile('wb', self.wbufsize) # wbufsize: 0  无缓冲

    protocol_version = "HTTP/1.0" # 1.1 可以自动keepalive

    # The Message-like class used to parse headers
    MessageClass = mimetools.Message

    self.handle()
    self.finish()
    ```

3. handle()
    
    WSGIRequestHandler - handler():
    ```
    self.raw_requestline = self.rfile.readline(65537) #GET / HTTP/1.1

    parse_request:
        self.command = None
        self.request_version = version = "HTTP/0.9"
        self.close_connection = 1
        self.requestline = self.raw_requestline.rstrip('\r\n') #删除尾部的\r\n
        words = ['GET', '/', 'HTTP/1.1']
        version_number = (1, 1)
        self.command = 'GET'
        self.path = '/'
        self.request_version = 'HTTP/1.1'
        self.headers = self.MessageClass(self.rfile, 0)

        headers:
        {
            'fp': <socket._fileobject object at 0x00000000032575E8>, 'status': '', 
            'startofbody': None, 
            'startofheaders': None, 
            'subtype': 'plain', 
            'type': 'text/plain', 
            'maintype': 'text', 
            'headers': [
                'Host: 127.0.0.1:8080\r\n', 
                'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64;x64; rv:60.0) Gecko/20100101 Firefox/60.0\r\n', 
                'Accept: text/html,application/xhtml+xml,  application/xml;q=0.9,*/*;q=0.8\r\n', 'Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2\r\n',
                'Accept-Encoding: gzip, deflate\r\n', 
                'Connection: keep-alive\r\n', 'Upgrade-Insecure-Requests: 1\r\n', 
                'Cache-Control: max-age=0\r\n'
                ], 
            'dict': {
                'accept-language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 
                'accept-encoding': 'gzip, deflate', 
                'host': '127.0.0.1:8080', 
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
                'connection': 'keep-alive', 
                'cache-control': 'max-age=0', 'upgrade-insecure-requests': '1'
                }, 
            'typeheader': None, 
            'encodingheader': None, 
            'seekable': 0, 
            'unixfrom': '', 'plisttext': '', 'plist': []
        }

    get_environ:
        env['SERVER_NAME'] = self.server_name 
        env['GATEWAY_INTERFACE'] = 'CGI/1.1'
        env['SERVER_PORT'] = str(self.server_port)
        env['REMOTE_HOST']=''
        env['CONTENT_LENGTH']=''
        env['SCRIPT_NAME'] = ''
        env['SERVER_PROTOCOL'] = "WSGIServer/" + __version__
        env['REQUEST_METHOD'] = self.command #GET
        env['PATH_INFO'] = urllib.unquote(path)
        env['QUERY_STRING'] = query # path中有?时
        env['REMOTE_HOST'] = 'localhost.localdomain' # socket.getfqdn('127.0.0.1')
        env['REMOTE_ADDR'] = self.client_address[0] # 127.0.0.1
        env['CONTENT_TYPE'] = 'text/plain'

        env[HTTP_ + headers[headers][key]] = value
    ```

4.  handler 实例
    ```
     handler = ServerHandler(
            self.rfile, self.wfile, sys.stderr, self.get_environ()
        )
    handler.run
    handler.request_handler = self      # backpointer for logging
    handler.run(self.server.get_app())
    ```

    初始化：
    ```
    self.stdin = rfile
    self.stdout = wfile
    self.stderr = sys.stderr,
    self.base_env = env
    self.wsgi_multithread = True
    self.wsgi_multiprocess = True
    ```
    run:
    ```
    env['wsgi.input']        = self.get_stdin()
    env['wsgi.errors']       = self.get_stderr()
    env['wsgi.version']      = self.wsgi_version
    env['wsgi.run_once']     = self.wsgi_run_once
    env['wsgi.url_scheme']   = self.get_scheme()
    env['wsgi.multithread']  = self.wsgi_multithread
    env['wsgi.multiprocess'] = self.wsgi_multiprocess

    ```
