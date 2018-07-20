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
    # =====  self.setup_environ() ==
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
    
    self.finish_response()
    ```



#### `Bottle.__call__ ,__handle, __cast, `

触发了Bottle的`__call__` 

`return self.wsgi(environ, start_response)`  每个实例都是一个a WSGI application, wsgi:

```python
out = self._cast(self.__handle(environ))

def __handle(environ):
    path = environ['bottle.raw_path'] = environ['PATH_INFO'] #/
    environ['bottle.app'] = self # Bottle
    request.bind(environ) # BaseRequest.__init__(environ) 
    response.bind() # BaseRespones.__init__() 
    # 这里都执行了intit但是不知道赋值给了谁， request 和 response 早已经实例化过了。
    # 下一步是执行了trigger_hook, 我们有必要看一看
     try:
                self.trigger_hook('before_request')
                route, args = self.router.match(environ) #在后面
                environ['route.handle'] = route
                environ['bottle.route'] = route
                environ['route.url_args'] = args
                return route.call(**args) # 这里注意：这里很特殊
            	# 去Route里看它的call方法， 
                # route.call 是被装饰的函数
                # route.call(**args) 这里就将这个被装饰的函数执行了。
                # 返回了执行的return.
            finally:
                self.trigger_hook('after_request')
```

hook:

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

下一步走到了router.match (environ)， 在下步之前， 建议先看下装饰器路由的初始化



#### router.match(environ)

```python
    router = Router() # 之前在
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
                target, getargs = self.static[method][path]  #  (<GET '/set' <function set at 0x00000000041A7128>>, None)，  这里target是个有被装饰函数的Route对象， 这里返回去了
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



在`__handle` 返回的`route.call(**args)` ，拿到被装饰的函数的返回值后， 传递给`__cast`: 

```python
    def _cast(self, out, peek=None): # out是返回值， '假定为个字符串'
       
        """ Try to convert the parameter into something WSGI compatible and set
        correct HTTP headers when possible.
        Support: False, str, unicode, dict, HTTPResponse, HTTPError, file-like,
        iterable of strings and iterable of unicodes
        """
        # Empty output is done here
        if not out:
            if 'Content-Length' not in response:
                response['Content-Length'] = 0
            return [] #呵，如果返回None,''等，它直接给赋成[]
        # Join lists of byte or unicode strings. Mixed lists are NOT supported
        if isinstance(out, (tuple, list))\
        and isinstance(out[0], (bytes, unicode)):
            out = out[0][0:0].join(out) # b'abc'[0:0] -> b''
        # Encode unicode strings
        if isinstance(out, unicode):
            out = out.encode(response.charset)
        # Byte Strings are just returned
        if isinstance(out, bytes):
            if 'Content-Length' not in response:
                response['Content-Length'] = len(out)
            return [out]   # 如是字符串的话： 'yyy', 这里就返回了[yyy]
        # HTTPError or HTTPException (recursive, because they may wrap anything)
        # TODO: Handle these explicitly in handle() or make them iterable.
        if isinstance(out, HTTPError):
            out.apply(response)
            out = self.error_handler.get(out.status_code, self.default_error_handler)(out)
            return self._cast(out)
        if isinstance(out, HTTPResponse):
            out.apply(response)
            return self._cast(out.body)

        # File-like objects.
        if hasattr(out, 'read'):
            if 'wsgi.file_wrapper' in request.environ:
                return request.environ['wsgi.file_wrapper'](out)
            elif hasattr(out, 'close') or not hasattr(out, '__iter__'):
                return WSGIFileWrapper(out)

        # Handle Iterables. We peek into them to detect their inner type.
        try:
            iout = iter(out)
            first = next(iout)
            while not first:
                first = next(iout)
        except StopIteration:
            return self._cast('')
        except HTTPResponse:
            first = _e()
        except (KeyboardInterrupt, SystemExit, MemoryError):
            raise
        except Exception:
            if not self.catchall: raise
            first = HTTPError(500, 'Unhandled exception', _e(), format_exc())

        # These are the inner types allowed in iterator or generator objects.
        if isinstance(first, HTTPResponse):
            return self._cast(first)
        elif isinstance(first, bytes):
            new_iter = itertools.chain([first], iout)
        elif isinstance(first, unicode):
            encoder = lambda x: x.encode(response.charset)
            new_iter = imap(encoder, itertools.chain([first], iout))
        else:
            msg = 'Unsupported response type: %s' % type(first)
            return self._cast(HTTPError(500, msg))
        if hasattr(out, 'close'):
            new_iter = _closeiter(new_iter, out.close)
        return new_iter
```





====   分割线 ===



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

一些理解：

```python
参数：
1. path, 可以没有，那么就映射成函数的名字。 还可以传入list: @get(['/index1', '/index2'])
2. method 也可以传入多个， 当然人本身是个list, 只是我们一直用的一个方法。
3. callback 不用转装饰器。eg;
	def func():
    	print 'this is a func'
	route('/index', callback=func)
    这在组织代码的时候比较方便
4. name, 默认没有为none, 我想这个是为管理route打tag而用的。
5. apply,
6. skip,
7. addition keyword
逻辑：
decorator(callback)的callback是指被装饰的函数。
获取路径和method 执行Route()
self.add_route()

def add_route(self, route):
    ''' Add a route object, but do not change the :data:`Route.app`
            attribute.'''
    self.routes.append(route)
    self.router.add(route.rule, route.method, route, name=route.name)
```



#### Route

```python
class Route(object):
    ''' This class wraps a route callback along with route specific metadata and
        configuration and applies Plugins on demand. It is also responsible for
        turing an URL path rule into a regular expression usable by the Router.
    '''

    def __init__(self, app, rule, method, callback, name=None,
                 plugins=None, skiplist=None, **config):
        #: The application this route is installed to.
        self.app = app
        #: The path-rule string (e.g. ``/wiki/:page``).
        self.rule = rule
        #: The HTTP method as a string (e.g. ``GET``).
        self.method = method
        #: The original callback with no plugins applied. Useful for introspection.
        self.callback = callback
        #: The name of the route (if specified) or ``None``.
        self.name = name or None
        #: A list of route-specific plugins (see :meth:`Bottle.route`).
        self.plugins = plugins or []
        #: A list of plugins to not apply to this route (see :meth:`Bottle.route`).
        self.skiplist = skiplist or []
        #: Additional keyword arguments passed to the :meth:`Bottle.route`
        #: decorator are stored in this dictionary. Used for route-specific
        #: plugin configuration and meta-data.
        self.config = ConfigDict().load_dict(config, make_namespaces=True)

    def __call__(self, *a, **ka):
        depr("Some APIs changed to return Route() instances instead of"\
             " callables. Make sure to use the Route.call method and not to"\
             " call Route instances directly.") #0.12
        return self.call(*a, **ka)
    
    @cached_property
    def call(self):
        ''' The route callback with all plugins applied. This property is
            created on demand and then cached to speed up subsequent requests.'''
        return self._make_callback()
    
    def _make_callback(self):
        callback = self.callback
        for plugin in self.all_plugins():
            try:
                if hasattr(plugin, 'apply'):
                    api = getattr(plugin, 'api', 1)
                    context = self if api > 1 else self._context
                    callback = plugin.apply(callback, context)
                else:
                    callback = plugin(callback)

            except RouteReset: # Try again with changed configuration.
                return self._make_callback()
            if not callback is self.callback:
                update_wrapper(callback, self.callback)
        return callback
```

call那里添加了@cached_property, 我们可以认为在调用Router.call时会触发, cached_property 的`__get__` 方法， 注意：Router.call和Router.call()是不一样的。

在handle的第五点中 `return route.call(**args）`中， route.call 返回的是被装饰的函数， 那么route.call(**args)则是这个被装饰函数的调用。



cached_property:

```python
class cached_property(object):
    ''' A property that is only computed once per instance and then replaces
        itself with an ordinary attribute. Deleting the attribute resets the
        property. '''

    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func

    def __get__(self, obj, cls):
        if obj is None: return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value
```





#### Router.add

接上：

```
self.routes.append(route)
self.router.add(route.rule, route.method, route, name=route.name)
```

routes 是个[], route 是个Route实例。

router 是个Router(),  Router实例， 这里执行Router.add()  #add('/index', 'GET', router, None)， 注意这个route,让我丢了好久， touter 是个类，虽然看起来是废话， 由于调试器的异样异样输出，我一直以为他是个function,往下看就清楚了。

```python
 def add(self, rule, method, target, name=None):
        ''' Add a new rule or replace the target for an existing rule. '''
        anons     = 0    # Number of anonymous wildcards found
        keys      = []   # Names of keys
        pattern   = ''   # Regular expression pattern with named groups
        filters   = []   # Lists of wildcard input filters
        builder   = []   # Data structure for the URL builder
        is_static = True

        for key, mode, conf in self._itertokens(rule): # 这里一个很恶心的正则， 
            #我们知道这里只返回 '/index', None, None
            if mode:
                is_static = False
                if mode == 'default': mode = self.default_filter
                mask, in_filter, out_filter = self.filters[mode](conf)
                if not key:
                    pattern += '(?:%s)' % mask
                    key = 'anon%d' % anons
                    anons += 1
                else:
                    pattern += '(?P<%s>%s)' % (key, mask)
                    keys.append(key)
                if in_filter: filters.append((key, in_filter))
                builder.append((key, out_filter or str))
            elif key:                     # 走这里
                pattern += re.escape(key) # 转义： \/index
                builder.append((None, key)) # [(None, ('/index')]

        self.builder[rule] = builder # builer['/index'] = [(None, ('/index')]
        if name: self.builder[name] = builder

        if is_static and not self.strict_order: # 会走这里的
            self.static.setdefault(method, {})  # self.static={'GET': {}}
            self.static[method][self.build(rule)] = (target, None) # {'GET': {'/set': (<GET '/set' <function set at 0x00000000041A7128>>, None)}}
            return
```

到这里一个@get 就完成了， 就可以注册执行下一个@get

注意这里的target 是Route类初始化返回 的route类，注意是个类，不要看debugger 出` (<GET '/set' <function set at 0x00000000041A7128>>, None)` 这里元祖第一个，也就是:` <GET '/set' <function set at 0x00000000041A7128>>`  是个route类，这些多都是传递的参数。不要被这个fucntion弄乱了。




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




### other get

```python
from Bottle import app
pprint.pprint(app().__dict__)

out:
 {'_hooks': {'after_request': [],
            'app_reset': [],
            'before_request': [],
            'config': []},
 'config': {'autojson': True, 'catchall': True},
 'error_handler': {},
 'plugins': [<bottle.JSONPlugin object at 0x000000000345AFD0>,
             <bottle.TemplatePlugin object at 0x000000000346C048>],
 'resources': <bottle.ResourceManager object at 0x000000000345AF28>,
 'router': <bottle.Router object at 0x000000000345AF60>,
 'routes': [<GET '/set' <function set at 0x0000000003464668>>,
            <GET '/get' <function get at 0x0000000003464748>>]}
```

