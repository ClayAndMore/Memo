###  流程

#### bottle.py

在导入botlle时， 就执行了bottle中代码：

```python
__author__ = 'Marcel Hellkamp'
__version__ = '0.12.13'
__license__ = 'MIT'

def make_default_app_wrapper(name):
    ''' Return a callable that relays calls to the current default app. '''
    @functools.wraps(getattr(Bottle, name))
    def wrapper(*a, **ka):
        return getattr(app(), name)(*a, **ka)
    return wrapper

route     = make_default_app_wrapper('route')
get       = make_default_app_wrapper('get')
post      = make_default_app_wrapper('post')
put       = make_default_app_wrapper('put')
delete    = make_default_app_wrapper('delete')
error     = make_default_app_wrapper('error')
mount     = make_default_app_wrapper('mount')
hook      = make_default_app_wrapper('hook')
install   = make_default_app_wrapper('install')
uninstall = make_default_app_wrapper('uninstall')
url       = make_default_app_wrapper('get_url')
```

全局变量：

```python
TEMPLATE_PATH = ['./', './views/']
TEMPLATES = {}
DEBUG = False
NORUN = False # If set, run() does nothing. Used by load_app()

#: A dict to map HTTP status codes (e.g. 404) to phrases (e.g. 'Not Found')
HTTP_CODES = httplib.responses
HTTP_CODES[418] = "I'm a teapot" # RFC 2324
HTTP_CODES[422] = "Unprocessable Entity" # RFC 4918
HTTP_CODES[428] = "Precondition Required"
HTTP_CODES[429] = "Too Many Requests"
HTTP_CODES[431] = "Request Header Fields Too Large"
HTTP_CODES[511] = "Network Authentication Required"
_HTTP_STATUS_LINES = dict((k, '%d %s'%(k,v)) for (k,v) in HTTP_CODES.items())

request = LocalRequest()
response = LocalResponse()
```



```python
def local_property(name=None):
    if name: depr('local_property() is deprecated and will be removed.') #0.12
    ls = threading.local()
    def fget(self):
        try: return ls.var
        except AttributeError:
            raise RuntimeError("Request context not initialized.")
    def fset(self, value): ls.var = value
    def fdel(self): del ls.var
    return property(fget, fset, fdel, 'Thread-local property')

class LocalRequest(BaseRequest):
    ''' A thread-local subclass of :class:`BaseRequest` with a different
        set of attributes for each thread. There is usually only one global
        instance of this class (:data:`request`). If accessed during a
        request/response cycle, this instance always refers to the *current*
        request (even on a multithreaded server). '''
    bind = BaseRequest.__init__
    environ = local_property()


class LocalResponse(BaseResponse):
    ''' A thread-local subclass of :class:`BaseResponse` with a different
        set of attributes for each thread. There is usually only one global
        instance of this class (:data:`response`). Its attributes are used
        to build the HTTP response at the end of the request/response cycle.
    '''
    bind = BaseResponse.__init__
    _status_line = local_property()
    _status_code = local_property()
    _cookies     = local_property()
    _headers     = local_property()
    body         = local_property()
    
Request = BaseRequest
Response = BaseResponse
```

到这里Request和Response都没有实例化

#### BaseRequest(object)

```python
class BaseRequest(object):
    def __init__(self, environ=None):
        """ Wrap a WSGI environ dictionary. """
        #: The wrapped WSGI environ dictionary. This is the only real attribute.
        #: All other attributes actually are read-only properties.
        self.environ = {} if environ is None else environ
        self.environ['bottle.request'] = self
    
	下面是由 @property 或 @DictProperty实现 的方法，我们可以按照类的属性来读， DictProperty是bottle定义的方式，和property 区别是它只是可读的
    
    - path   路径
    - method 请求方法
    - get_header 
    - get_cookie
    - body
    - chunked
    - POST
    - url
    - content_length
    - content_type
    - remote_addr

    @property
    def method(self):
        return self.environ.get('REQUEST_METHOD', 'GET').upper()
    
    def get_header(self, name, default=None):
        ''' Return the value of a request header, or a given default value. '''
        return self.headers.get(name, default)
    
    def get_cookie(self, key, default=None, secret=None):
        """ Return the content of a cookie. To read a `Signed Cookie`, the
            `secret` must match the one used to create the cookie (see
            :meth:`BaseResponse.set_cookie`). If anything goes wrong (missing
            cookie or wrong signature), return a default value. """
        value = self.cookies.get(key)
        if secret and value:
            dec = cookie_decode(value, secret) # (key, value) tuple or None
            return dec[1] if dec and dec[0] == key else default
        return value or default
```





#### BaseResponse(object)

```python
   def __init__(self, body='', status=None, headers=None, **more_headers):
        self._cookies = None
        self._headers = {}
        self.body = body
        self.status = status or self.default_status
        if headers:
            if isinstance(headers, dict):
                headers = headers.items()
            for name, value in headers:
                self.add_header(name, value)
        if more_headers:
            for name, value in more_headers.items():
                self.add_header(name, value)
```





app 栈：

```python
#: A thread-safe namespace. Not used by Bottle. 
# 一个线程安全空间， bottle并没有用上
local = threading.local()

app = default_app = AppStack() # app = defautl_app = []

class AppStack(list):
    """ A stack-like list. Calling it returns the head of the stack. """

    def __call__(self):
        """ Return the current default application. """
        return self[-1]

    def push(self, value=None):
        """ Add a new :class:`Bottle` instance to the stack """
        if not isinstance(value, Bottle):
            value = Bottle()
        self.append(value)
        return value
app.push
```

AppStack 就是封装了list， 现在app是个[Bottle(),]

#### Bottle()

```python
    def __init__(self, catchall=True, autojson=True):

        #: A :class:`ConfigDict` for app specific configuration.
        self.config = ConfigDict()
        self.config._on_change = functools.partial(self.trigger_hook, 'config')
        self.config.meta_set('autojson', 'validate', bool)
        self.config.meta_set('catchall', 'validate', bool)
        self.config['catchall'] = catchall
        self.config['autojson'] = autojson

        #: A :class:`ResourceManager` for application files
        self.resources = ResourceManager()

        self.routes = [] # List of installed :class:`Route` instances.
        self.router = Router() # Maps requests to :class:`Route` instances.
        self.error_handler = {}

        # Core plugins
        self.plugins = [] # List of installed plugins.
        if self.config['autojson']:
            self.install(JSONPlugin())
        self.install(TemplatePlugin())
```

注意router



#### Router()

```python

    def __init__(self, strict=False):
        self.rules    = [] # All rules in order
        self._groups  = {} # index of regexes to find them in dyna_routes
        self.builder  = {} # Data structure for the url builder
        self.static   = {} # Search structure for static routes
        self.dyna_routes   = {}
        self.dyna_regexes  = {} # Search structure for dynamic routes
        #: If true, static routes are no longer checked first.
        self.strict_order = strict
        self.filters = {
            're':    lambda conf:
                (_re_flatten(conf or self.default_pattern), None, None),
            'int':   lambda conf: (r'-?\d+', int, lambda x: str(int(x))),
            'float': lambda conf: (r'-?[\d.]+', float, lambda x: str(float(x))),
            'path':  lambda conf: (r'.+?', None, None)}

```







#### Server

bottle.run():

0. app的生成：

   ```python
   app = Bottle() #上方初始化 default_app() -> __call__ -> Bottle()
   ```


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
    执行WSGIRefServer.run(app)  (bottle.run的直接转化)

2. WSGIRefServer run()里规定了FixedHandler类， 通过wsgiref.simple_server的make_server 方法实现了server类的初始化：
    `WSGIServer((host,port),FixedHandler).server_forever()`

    host='127.0.0.1', port=8080

3. WSGIServer --> TCPServer(__init__) --> BaseServer(__init__)
    ```
        self.server_address = (host, port)
        self.RequestHandlerClass = FixedHandler
        self.__is_shut_down = threading.Event()
        self.__shutdown_request = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
    
        self.server_bind()
        self.server_activate() # self.socket.listen(5)
    ```

 4. init过程中用到了server_bind()
    server_bind(): WSGIServer, HTTPServer, TCPServer
    ```
        socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 操作系统会在服务器socket被关闭或服务器进程终止后马上释放该服务器的端口，否则操作系统会保留几分钟该端口。
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

    make_server() 中： 

    ```python
    set_app (app)-> WSGIServer().application = app # Bottle
    
    ```

    make_server 完成。

5. WSGIServer.serve_forever() # 

    ```python
    # class BaseServer
    def server_forever(self, poll_interval=0.5):
        self.__is_shut_down.clear() #threading.Event().clear() , 这里flag为1
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

    threading.Event().clear()  让线程非阻塞

    `r, w, e = select.select([self], [], [], 0.5)`  0.5秒的轮询.
    等待 r 可读缓冲区有值


#### handle

1. 接上， 我们访问根路由， 缓冲区有值时 _handle_request_noblock():
    ```python
    request, client_address = self.socket.accept() # request: socket._socketobject client_address: ('127.0.0.1', 38419) 本地windows平台浏览器设置
    # finish_request-> 初始化HandlerClass, 接受一个请求初始一个Handler
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
    MessageClass = mimetools.Message(rfc822.Message)
    
    self.handle()
    self.finish()
    ```

3. handle()

    WSGIRequestHandler - handler():
    ```python
    self.raw_requestline = self.rfile.readline(65537) #GET / HTTP/1.1
    
    # 检查有收入块没有错误代码的函数
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
    	
        self.headers 如下， 每次都是read line最后存在MessageClass里。
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
    
    	因为keep-alive, 使得elf.close_connection = 0
    
    get_environ:
        env = self.server.base_environ.copy()
        #{'CONTENT_LENGTH': '',
        # 'GATEWAY_INTERFACE': 'CGI/1.1',
        # 'REMOTE_HOST': '',
        # 'REQUEST_METHOD': 'GET',
        # 'SCRIPT_NAME': '',
        # 'SERVER_NAME': 'DESKTOP-4FSTEEM',
        # 'SERVER_PORT': '8080',
        # 'SERVER_PROTOCOL': 'HTTP/1.1'}
        env['SERVER_PROTOCOL'] = self.request_version # 'HTTP/1.1'
        env['REQUEST_METHOD'] = self.command # 'GET'
        env['PATH_INFO'] = '/'
        env['QUERY_STRING'] = ''
        env['REMOTE_ADDR'] = '127.0.0.1'
        env['CONTENT_TYPE'] = self.headers.type
        # env['CONTENT_LENGTH'] = self.headers.get('content-length')
        header.header中遍历-> env['HTTP_HOST']=127.0.0.1 都这样转化
        
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

4. handler 实例
    ```python
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
    (BaseHandler) run(self, application):
    ```python
    env = self.environ = self.os_environ.copy() # dict(os.environ.items())
    self.environ.update(env)
    
    env['wsgi.input']        = self.get_stdin()
    env['wsgi.errors']       = self.get_stderr()
    env['wsgi.version']      = self.wsgi_version # (1, 0)
    env['wsgi.run_once']     = self.wsgi_run_once # False
    env['wsgi.url_scheme']   = self.get_scheme() # https or http
    env['wsgi.multithread']  = self.wsgi_multithread #True
    env['wsgi.multiprocess'] = self.wsgi_multiprocess # False
    env['wsgi.file_wrapper'] = util.FileWrapper
    env['SERVER_SOFTWARE']   = "WSGIServer/" + __version__ + "Python/" + sys.version.split()[0]
    
    self.result = application(self.environ, self.start_response) # BaseHandler的start_response 方法, 注意application 是Bottle实例, 此时这里执行的就是Bottle()(self.environ, self.start_response), 这会触发Bottle的__call__方法。
       
    ```

5. 触发了Bottle的`__call__` 

    `return self.wsgi(environ, start_response)`  每个实例都是一个a WSGI application, wsgi:

    ```python
    out = self._cast(slef.__handle(environ))
    
    def __handle(environ):
        path = environ['bottle.raw_path'] = environ['PATH_INFO'] #/
        environ['bottle.app'] = self # Bottle
        request.bind(environ) # BaseRequest.__init__(environ) 
        response.bind() # BaseRespones.__init__() 
    ```

    这里都执行了intit但是不知道赋值给了谁， request 和 response 早已经实例化过了。

    下一步是执行了trigger_hook, 我们有必要看一看

     ```python
    self.trigger_hook('before_request')
    
    def trigger_hook(self, __name, *args, **kwargs):
      ''' Trigger a hook and return a list of results. '''
        return [hook(*args, **kwargs) for hook in self._hooks[__name][:]]
    
    def _hooks(self):
        return dict((name, []) for name in self.__hook_names)

     __hook_names = 'before_request', 'after_request', 'app_reset', 'config'

     def hook(self, name):
     """ Return a decorator that attaches a callback to a hook. See
                    :meth:`add_hook` for details."""
          def decorator(func):
              self.add_hook(name, func)
                  return func
           return decorator
    
    def add_hook(self, name, func):
        if name in self.__hook_reversed:
             self._hooks[name].insert(0, func)
        else:
             self._hooks[name].append(func)
     ```
    
    有一个hook列表， 在请求前的hook，一般没有加func就为[], 其他也是，如果有则执行func(*args, **kwargs)
    
    ​ 下一步走到了router.match (environ)

#### router.match(environ)

```python
    router = Router() #
    def match(self, environ):
        ''' Return a (target, url_agrs) tuple or raise HTTPError(400/404/405). '''
        verb = environ['REQUEST_METHOD'].upper()
        path = environ['PATH_INFO'] or '/'
        target = None
        if verb == 'HEAD':
            methods = ['PROXY', verb, 'GET', 'ANY']
        else:
            methods = ['PROXY', verb, 'ANY']

        for method in methods:
            if method in self.static and path in self.static[method]:
                target, getargs = self.static[method][path]
                return target, getargs(path) if getargs else {}
            elif method in self.dyna_regexes:
                for combined, rules in self.dyna_regexes[method]:
                    match = combined(path)
                    if match:
                        target, getargs = rules[match.lastindex - 1]
                        return target, getargs(path) if getargs else {}
    
        # No matching route found. Collect alternative methods for 405 response
        allowed = set([])
        nocheck = set(methods)
        for method in set(self.static) - nocheck:
            if path in self.static[method]:
                allowed.add(verb)
        for method in set(self.dyna_regexes) - allowed - nocheck:
            for combined, rules in self.dyna_regexes[method]:
                match = combined(path)
                if match:
                    allowed.add(method)
        if allowed:
            allow_header = ",".join(sorted(allowed))
            raise HTTPError(405, "Method not allowed.", Allow=allow_header)
    
        # No matching route and no alternative method found. We give up
        raise HTTPError(404, "Not found: " + repr(path))
```



####  装饰器路由的初始化 

@get为例：

```python
from bottle import get
@get('/index')
def home():
    return 'hhhh'

## bottle 文件中
get = make_default_app_wrapper('get')

def make_default_app_wrapper(name):
    ''' Return a callable that relays calls to the current default app. '''
    @functools.wraps(getattr(Bottle, name))
    def wrapper(*a, **ka):
        return getattr(app(), name)(*a, **ka)
    return wrapper

## 最后：
app() 是第一个Bottle()， 就是上方的AppStack.push()
getattr(app(), 'get') ==> Bottle.get

def get(self, path=None, method='GET', **options):
     """ Equals :meth:`route`. """
     return self.route(path, method, **options)

get(path='/index', method='GET', **options)
# 走的route(), 基本所有方法都会走route()
# 那是不是直接用route会快那么一点点。。
```



#### route()   

```python
	def route(self, path=None, method='GET', callback=None, name=None,
              apply=None, skip=None, **config):
        """ A decorator to bind a function to a request URL. Example::

                @app.route('/hello/:name')
                def hello(name):
                    return 'Hello %s' % name
    
            The ``:name`` part is a wildcard. See :class:`Router` for syntax
            details.
    
            :param path: Request path or a list of paths to listen to. If no
              path is specified, it is automatically generated from the
              signature of the function.
            :param method: HTTP method (`GET`, `POST`, `PUT`, ...) or a list of
              methods to listen to. (default: `GET`)
            :param callback: An optional shortcut to avoid the decorator
              syntax. ``route(..., callback=func)`` equals ``route(...)(func)``
            :param name: The name for this route. (default: None)
            :param apply: A decorator or plugin or a list of plugins. These are
              applied to the route callback in addition to installed plugins.
            :param skip: A list of plugins, plugin classes or names. Matching
              plugins are not installed to this route. ``True`` skips all.
    
            Any additional keyword arguments are stored as route-specific
            configuration and passed to plugins (see :meth:`Plugin.apply`).
        """
        if callable(path): path, callback = None, path
        plugins = makelist(apply)
        skiplist = makelist(skip)
        def decorator(callback):
            # TODO: Documentation and tests
            if isinstance(callback, basestring): callback = load(callback)
            for rule in makelist(path) or yieldroutes(callback):
                for verb in makelist(method):
                    verb = verb.upper()
                    route = Route(self, rule, verb, callback, name=name,
                                  plugins=plugins, skiplist=skiplist, **config)
                    self.add_route(route)
            return callback
        return decorator(callback) if callback else decorator
```










    看下BaseHandler的start_response 方法：
    
    ```python
        def start_response(self, status, headers,exc_info=None):
            """'start_response()' callable as specified by PEP 333"""
    
            if exc_info:
                try:
                    if self.headers_sent:
                        # Re-raise original exception if headers sent
                        raise exc_info[0], exc_info[1], exc_info[2]
                finally:
                    exc_info = None        # avoid dangling circular ref
            elif self.headers is not None:
                raise AssertionError("Headers already set!")
    
            assert type(status) is StringType,"Status must be a string"
            assert len(status)>=4,"Status must be at least 4 characters"
            assert int(status[:3]),"Status message must begin w/3-digit code"
            assert status[3]==" ", "Status message must have a space after code"
            if __debug__:
                for name,val in headers:
                    assert type(name) is StringType,"Header names must be strings"
                    assert type(val) is StringType,"Header values must be strings"
                    assert not is_hop_by_hop(name),"Hop-by-hop headers not allowed"
            self.status = status
            self.headers = self.headers_class(headers)
            return self.write