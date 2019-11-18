# ======== bottle.py =============
class FixedHandler(WSGIRequestHandler):
    def address_string(self): # Prevent reverse DNS lookups please.
        return self.client_address[0]
    def log_request(*args, **kw):
        if not self.quiet:
            return WSGIRequestHandler.log_request(*args, **kw)


# ========= wsgiref/simple_server.py  =========
class WSGIRequestHandler(BaseHTTPRequestHandler):

    server_version = "WSGIServer/" + __version__

    def get_environ(self):
        env = self.server.base_environ.copy()
        env['SERVER_PROTOCOL'] = self.request_version
        env['REQUEST_METHOD'] = self.command
        if '?' in self.path:
            path,query = self.path.split('?',1)
        else:
            path,query = self.path,''

        env['PATH_INFO'] = urllib.unquote(path)
        env['QUERY_STRING'] = query

        host = self.address_string()
        if host != self.client_address[0]:
            env['REMOTE_HOST'] = host
        env['REMOTE_ADDR'] = self.client_address[0]

        if self.headers.typeheader is None:
            env['CONTENT_TYPE'] = self.headers.type
        else:
            env['CONTENT_TYPE'] = self.headers.typeheader

        length = self.headers.getheader('content-length')
        if length:
            env['CONTENT_LENGTH'] = length

        for h in self.headers.headers:
            k,v = h.split(':',1)
            k=k.replace('-','_').upper(); v=v.strip()
            if k in env:
                continue                    # skip content length, type,etc.
            if 'HTTP_'+k in env:
                env['HTTP_'+k] += ','+v     # comma-separate multiple headers
            else:
                env['HTTP_'+k] = v
        return env

    def get_stderr(self):
        return sys.stderr

    def handle(self):
        """Handle a single HTTP request"""

        self.raw_requestline = self.rfile.readline(65537)
        if len(self.raw_requestline) > 65536:
            self.requestline = ''
            self.request_version = ''
            self.command = ''
            self.send_error(414)
            return

        if not self.parse_request(): # An error code has been sent, just exit
            return

        handler = ServerHandler(
            self.rfile, self.wfile, self.get_stderr(), self.get_environ()
        )
        handler.request_handler = self      # backpointer for logging
        handler.run(self.server.get_app()

class ServerHandler(SimpleHandler):

    server_software = software_version

    def close(self):
        try:
            self.request_handler.log_request(
                self.status.split(' ',1)[0], self.bytes_sent
            )
        finally:
            SimpleHandler.close(self)


# ========== wsgiref/handlers.py =======
class SimpleHandler(BaseHandler):
    """Handler that's just initialized with streams, environment, etc.

    This handler subclass is intended for synchronous HTTP/1.0 origin servers,
    and handles sending the entire response output, given the correct inputs.

    Usage::

        handler = SimpleHandler(
            inp,out,err,env, multithread=False, multiprocess=True
        )
        handler.run(app)"""

    def __init__(self,stdin,stdout,stderr,environ,
        multithread=True, multiprocess=False
    ):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.base_env = environ
        self.wsgi_multithread = multithread
        self.wsgi_multiprocess = multiprocess

    def get_stdin(self):
        return self.stdin

    def get_stderr(self):
        return self.stderr

    def add_cgi_vars(self):
        self.environ.update(self.base_env)

    def _write(self,data):
        self.stdout.write(data)
        self._write = self.stdout.write

    def _flush(self):
        self.stdout.flush()
        self._flush = self.stdout.flush
    
class BaseHandler:
    """Manage the invocation of a WSGI application"""

    # Configuration parameters; can override per-subclass or per-instance
    wsgi_version = (1,0)
    wsgi_multithread = True
    wsgi_multiprocess = True
    wsgi_run_once = False

    origin_server = True    # We are transmitting direct to client
    http_version  = "1.0"   # Version that should be used for response
    server_software = None  # String name of server software, if any

    # os_environ is used to supply configuration from the OS environment:
    # by default it's a copy of 'os.environ' as of import time, but you can
    # override this in e.g. your __init__ method.
    os_environ = dict(os.environ.items())

    # Collaborator classes
    wsgi_file_wrapper = FileWrapper     # set to None to disable
    headers_class = Headers             # must be a Headers-like class

    # Error handling (also per-subclass or per-instance)
    traceback_limit = None  # Print entire traceback to self.get_stderr()
    error_status = "500 Internal Server Error"
    error_headers = [('Content-Type','text/plain')]
    error_body = "A server error occurred.  Please contact the administrator."

    # State variables (don't mess with these)
    status = result = None
    headers_sent = False
    headers = None
    bytes_sent = 0

    def run(self, application):
        """Invoke the application"""
        # Note to self: don't move the close()!  Asynchronous servers shouldn't
        # call close() from finish_response(), so if you close() anywhere but
        # the double-error branch here, you'll break asynchronous servers by
        # prematurely closing.  Async servers must return from 'run()' without
        # closing if there might still be output to iterate over.
        try:
            self.setup_environ()
            self.result = application(self.environ, self.start_response)
            self.finish_response()
        except:
            try:
                self.handle_error()
            except:
                # If we get an error handling an error, just give up already!
                self.close()
                raise   # ...and let the actual server figure it out.


    def setup_environ(self):
        """Set up the environment for one request"""

        env = self.environ = self.os_environ.copy()
        self.add_cgi_vars()

        env['wsgi.input']        = self.get_stdin()
        env['wsgi.errors']       = self.get_stderr()
        env['wsgi.version']      = self.wsgi_version
        env['wsgi.run_once']     = self.wsgi_run_once
        env['wsgi.url_scheme']   = self.get_scheme()
        env['wsgi.multithread']  = self.wsgi_multithread
        env['wsgi.multiprocess'] = self.wsgi_multiprocess

        if self.wsgi_file_wrapper is not None:
            env['wsgi.file_wrapper'] = self.wsgi_file_wrapper

        if self.origin_server and self.server_software:
            env.setdefault('SERVER_SOFTWARE',self.server_software)


    def finish_response(self):
        """Send any iterable data, then close self and the iterable

        Subclasses intended for use in asynchronous servers will
        want to redefine this method, such that it sets up callbacks
        in the event loop to iterate over the data, and to call
        'self.close()' once the response is finished.
        """
        try:
            if not self.result_is_file() or not self.sendfile():
                for data in self.result:
                    self.write(data)
                self.finish_content()
        finally:
            self.close()


    def get_scheme(self):
        """Return the URL scheme being used"""
        return guess_scheme(self.environ)


    def set_content_length(self):
        """Compute Content-Length or switch to chunked encoding if possible"""
        try:
            blocks = len(self.result)
        except (TypeError,AttributeError,NotImplementedError):
            pass
        else:
            if blocks==1:
                self.headers['Content-Length'] = str(self.bytes_sent)
                return
        # XXX Try for chunked encoding if origin server and client is 1.1


    def cleanup_headers(self):
        """Make any necessary header changes or defaults

        Subclasses can extend this to add other defaults.
        """
        if 'Content-Length' not in self.headers:
            self.set_content_length()

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


    def send_preamble(self):
        """Transmit version/status/date/server, via self._write()"""
        if self.origin_server:
            if self.client_is_modern():
                self._write('HTTP/%s %s\r\n' % (self.http_version,self.status))
                if 'Date' not in self.headers:
                    self._write(
                        'Date: %s\r\n' % format_date_time(time.time())
                    )
                if self.server_software and 'Server' not in self.headers:
                    self._write('Server: %s\r\n' % self.server_software)
        else:
            self._write('Status: %s\r\n' % self.status)

    def write(self, data):
        """'write()' callable as specified by PEP 333"""

        assert type(data) is StringType,"write() argument must be string"

        if not self.status:
            raise AssertionError("write() before start_response()")

        elif not self.headers_sent:
            # Before the first output, send the stored headers
            self.bytes_sent = len(data)    # make sure we know content-length
            self.send_headers()
        else:
            self.bytes_sent += len(data)

        # XXX check Content-Length and truncate if too many bytes written?
        self._write(data)
        self._flush()


    def sendfile(self):
        """Platform-specific file transmission

        Override this method in subclasses to support platform-specific
        file transmission.  It is only called if the application's
        return iterable ('self.result') is an instance of
        'self.wsgi_file_wrapper'.

        This method should return a true value if it was able to actually
        transmit the wrapped file-like object using a platform-specific
        approach.  It should return a false value if normal iteration
        should be used instead.  An exception can be raised to indicate
        that transmission was attempted, but failed.

        NOTE: this method should call 'self.send_headers()' if
        'self.headers_sent' is false and it is going to attempt direct
        transmission of the file.
        """
        return False   # No platform-specific transmission by default


    def finish_content(self):
        """Ensure headers and content have both been sent"""
        if not self.headers_sent:
            # Only zero Content-Length if not set by the application (so
            # that HEAD requests can be satisfied properly, see #3839)
            self.headers.setdefault('Content-Length', "0")
            self.send_headers()
        else:
            pass # XXX check if content-length was too short?

    def close(self):
        """Close the iterable (if needed) and reset all instance vars

        Subclasses may want to also drop the client connection.
        """
        try:
            if hasattr(self.result,'close'):
                self.result.close()
        finally:
            self.result = self.headers = self.status = self.environ = None
            self.bytes_sent = 0; self.headers_sent = False


    def send_headers(self):
        """Transmit headers to the client, via self._write()"""
        self.cleanup_headers()
        self.headers_sent = True
        if not self.origin_server or self.client_is_modern():
            self.send_preamble()
            self._write(str(self.headers))


    def result_is_file(self):
        """True if 'self.result' is an instance of 'self.wsgi_file_wrapper'"""
        wrapper = self.wsgi_file_wrapper
        return wrapper is not None and isinstance(self.result,wrapper)


    def client_is_modern(self):
        """True if client can accept status and headers"""
        return self.environ['SERVER_PROTOCOL'].upper() != 'HTTP/0.9'


    def log_exception(self,exc_info):
        """Log the 'exc_info' tuple in the server log

        Subclasses may override to retarget the output or change its format.
        """
        try:
            from traceback import print_exception
            stderr = self.get_stderr()
            print_exception(
                exc_info[0], exc_info[1], exc_info[2],
                self.traceback_limit, stderr
            )
            stderr.flush()
        finally:
            exc_info = None

    def handle_error(self):
        """Log current error, and send error output to client if possible"""
        self.log_exception(sys.exc_info())
        if not self.headers_sent:
            self.result = self.error_output(self.environ, self.start_response)
            self.finish_response()
        # XXX else: attempt advanced recovery techniques for HTML or text?

    def error_output(self, environ, start_response):
        """WSGI mini-app to create error output

        By default, this just uses the 'error_status', 'error_headers',
        and 'error_body' attributes to generate an output page.  It can
        be overridden in a subclass to dynamically generate diagnostics,
        choose an appropriate message for the user's preferred language, etc.

        Note, however, that it's not recommended from a security perspective to
        spit out diagnostics to any old user; ideally, you should have to do
        something special to enable diagnostic output, which is why we don't
        include any here!
        """
        start_response(self.error_status,self.error_headers[:],sys.exc_info())
        return [self.error_body]


    # Pure abstract methods; *must* be overridden in subclasses

    def _write(self,data):
        """Override in subclass to buffer data for send to client

        It's okay if this method actually transmits the data; BaseHandler
        just separates write and flush operations for greater efficiency
        when the underlying system actually has such a distinction.
        """
        raise NotImplementedError

    def _flush(self):
        """Override in subclass to force sending of recent '_write()' calls

        It's okay if this method is a no-op (i.e., if '_write()' actually
        sends the data.
        """
        raise NotImplementedError

    def get_stdin(self):
        """Override in subclass to return suitable 'wsgi.input'"""
        raise NotImplementedError

    def get_stderr(self):
        """Override in subclass to return suitable 'wsgi.errors'"""
        raise NotImplementedError

    def add_cgi_vars(self):
        """Override in subclass to insert CGI variables in 'self.environ'"""
        raise NotImplementedError


# ==========  BaseHTTPServer.py ===========

class BaseHTTPRequestHandler(SocketServer.StreamRequestHandler):

    # The Python system version, truncated to its first component.
    sys_version = "Python/" + sys.version.split()[0]

    # The server software version.  You may want to override this.
    # The format is multiple whitespace-separated strings,
    # where each string is of the form name[/version].
    server_version = "BaseHTTP/" + __version__

    # The default request version.  This only affects responses up until
    # the point where the request line is parsed, so it mainly decides what
    # the client gets back when sending a malformed request line.
    # Most web servers default to HTTP 0.9, i.e. don't send a status line.
    default_request_version = "HTTP/0.9"

    def parse_request(self):
        """Parse a request (internal).

        The request should be stored in self.raw_requestline; the results
        are in self.command, self.path, self.request_version and
        self.headers.

        Return True for success, False for failure; on failure, an
        error is sent back.

        """
        self.command = None  # set in case of error on the first line
        self.request_version = version = self.default_request_version
        self.close_connection = 1
        requestline = self.raw_requestline
        requestline = requestline.rstrip('\r\n')
        self.requestline = requestline
        words = requestline.split()
        if len(words) == 3:
            command, path, version = words
            if version[:5] != 'HTTP/':
                self.send_error(400, "Bad request version (%r)" % version)
                return False
            try:
                base_version_number = version.split('/', 1)[1]
                version_number = base_version_number.split(".")
                # RFC 2145 section 3.1 says there can be only one "." and
                #   - major and minor numbers MUST be treated as
                #      separate integers;
                #   - HTTP/2.4 is a lower version than HTTP/2.13, which in
                #      turn is lower than HTTP/12.3;
                #   - Leading zeros MUST be ignored by recipients.
                if len(version_number) != 2:
                    raise ValueError
                version_number = int(version_number[0]), int(version_number[1])
            except (ValueError, IndexError):
                self.send_error(400, "Bad request version (%r)" % version)
                return False
            if version_number >= (1, 1) and self.protocol_version >= "HTTP/1.1":
                self.close_connection = 0
            if version_number >= (2, 0):
                self.send_error(505,
                          "Invalid HTTP Version (%s)" % base_version_number)
                return False
        elif len(words) == 2:
            command, path = words
            self.close_connection = 1
            if command != 'GET':
                self.send_error(400,
                                "Bad HTTP/0.9 request type (%r)" % command)
                return False
        elif not words:
            return False
        else:
            self.send_error(400, "Bad request syntax (%r)" % requestline)
            return False
        self.command, self.path, self.request_version = command, path, version

        # Examine the headers and look for a Connection directive
        self.headers = self.MessageClass(self.rfile, 0)

        conntype = self.headers.get('Connection', "")
        if conntype.lower() == 'close':
            self.close_connection = 1
        elif (conntype.lower() == 'keep-alive' and
              self.protocol_version >= "HTTP/1.1"):
            self.close_connection = 0
        return True

    def handle_one_request(self):
        """Handle a single HTTP request.

        You normally don't need to override this method; see the class
        __doc__ string for information on how to handle specific HTTP
        commands such as GET and POST.

        """
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(414)
                return
            if not self.raw_requestline:
                self.close_connection = 1
                return
            if not self.parse_request():
                # An error code has been sent, just exit
                return
            mname = 'do_' + self.command
            if not hasattr(self, mname):
                self.send_error(501, "Unsupported method (%r)" % self.command)
                return
            method = getattr(self, mname)
            method()
            self.wfile.flush() #actually send the response if not already done.
        except socket.timeout, e:
            #a read or a write timed out.  Discard this connection
            self.log_error("Request timed out: %r", e)
            self.close_connection = 1
            return

    def handle(self):
        """Handle multiple requests if necessary."""
        self.close_connection = 1

        self.handle_one_request()
        while not self.close_connection:
            self.handle_one_request()

    def send_error(self, code, message=None):
        """Send and log an error reply.

        Arguments are the error code, and a detailed message.
        The detailed message defaults to the short entry matching the
        response code.

        This sends an error response (so it must be called before any
        output has been generated), logs the error, and finally sends
        a piece of HTML explaining the error to the user.

        """

        try:
            short, long = self.responses[code]
        except KeyError:
            short, long = '???', '???'
        if message is None:
            message = short
        explain = long
        self.log_error("code %d, message %s", code, message)
        self.send_response(code, message)
        self.send_header('Connection', 'close')

        # Message body is omitted for cases described in:
        #  - RFC7230: 3.3. 1xx, 204(No Content), 304(Not Modified)
        #  - RFC7231: 6.3.6. 205(Reset Content)
        content = None
        if code >= 200 and code not in (204, 205, 304):
            # HTML encode to prevent Cross Site Scripting attacks
            # (see bug #1100201)
            content = (self.error_message_format % {
                'code': code,
                'message': _quote_html(message),
                'explain': explain
            })
            self.send_header("Content-Type", self.error_content_type)
        self.end_headers()

        if self.command != 'HEAD' and content:
            self.wfile.write(content)

    error_message_format = DEFAULT_ERROR_MESSAGE
    error_content_type = DEFAULT_ERROR_CONTENT_TYPE

    def send_response(self, code, message=None):
        """Send the response header and log the response code.

        Also send two standard headers with the server software
        version and the current date.

        """
        self.log_request(code)
        if message is None:
            if code in self.responses:
                message = self.responses[code][0]
            else:
                message = ''
        if self.request_version != 'HTTP/0.9':
            self.wfile.write("%s %d %s\r\n" %
                             (self.protocol_version, code, message))
            # print (self.protocol_version, code, message)
        self.send_header('Server', self.version_string())
        self.send_header('Date', self.date_time_string())

    def send_header(self, keyword, value):
        """Send a MIME header."""
        if self.request_version != 'HTTP/0.9':
            self.wfile.write("%s: %s\r\n" % (keyword, value))

        if keyword.lower() == 'connection':
            if value.lower() == 'close':
                self.close_connection = 1
            elif value.lower() == 'keep-alive':
                self.close_connection = 0

    def end_headers(self):
        """Send the blank line ending the MIME headers."""
        if self.request_version != 'HTTP/0.9':
            self.wfile.write("\r\n")

    def log_request(self, code='-', size='-'):
        """Log an accepted request.

        This is called by send_response().

        """

        self.log_message('"%s" %s %s',
                         self.requestline, str(code), str(size))

    def log_error(self, format, *args):
        """Log an error.

        This is called when a request cannot be fulfilled.  By
        default it passes the message on to log_message().

        Arguments are the same as for log_message().

        XXX This should go to the separate error log.

        """

        self.log_message(format, *args)

    def log_message(self, format, *args):
        """Log an arbitrary message.

        This is used by all other logging functions.  Override
        it if you have specific logging wishes.

        The first argument, FORMAT, is a format string for the
        message to be logged.  If the format string contains
        any % escapes requiring parameters, they should be
        specified as subsequent arguments (it's just like
        printf!).

        The client ip address and current date/time are prefixed to every
        message.

        """

        sys.stderr.write("%s - - [%s] %s\n" %
                         (self.client_address[0],
                          self.log_date_time_string(),
                          format%args))

    def version_string(self):
        """Return the server software version string."""
        return self.server_version + ' ' + self.sys_version

    def date_time_string(self, timestamp=None):
        """Return the current date and time formatted for a message header."""
        if timestamp is None:
            timestamp = time.time()
        year, month, day, hh, mm, ss, wd, y, z = time.gmtime(timestamp)
        s = "%s, %02d %3s %4d %02d:%02d:%02d GMT" % (
                self.weekdayname[wd],
                day, self.monthname[month], year,
                hh, mm, ss)
        return s

    def log_date_time_string(self):
        """Return the current time formatted for logging."""
        now = time.time()
        year, month, day, hh, mm, ss, x, y, z = time.localtime(now)
        s = "%02d/%3s/%04d %02d:%02d:%02d" % (
                day, self.monthname[month], year, hh, mm, ss)
        return s

    weekdayname = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    monthname = [None,
                 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    def address_string(self):
        """Return the client address formatted for logging.

        This version looks up the full hostname using gethostbyaddr(),
        and tries to find a name that contains at least one dot.

        """

        host, port = self.client_address[:2]
        return socket.getfqdn(host)

    # Essentially static class variables

    # The version of the HTTP protocol we support.
    # Set this to HTTP/1.1 to enable automatic keepalive
    protocol_version = "HTTP/1.0"

    # The Message-like class used to parse headers
    MessageClass = mimetools.Message

    # Table mapping response codes to messages; entries have the
    # form {code: (shortmessage, longmessage)}.
    # See RFC 2616.
    responses = {
        100: ('Continue', 'Request received, please continue'),
        101: ('Switching Protocols',
              'Switching to new protocol; obey Upgrade header'),

        200: ('OK', 'Request fulfilled, document follows'),
        201: ('Created', 'Document created, URL follows'),
        202: ('Accepted',
              'Request accepted, processing continues off-line'),
        203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
        204: ('No Content', 'Request fulfilled, nothing follows'),
        205: ('Reset Content', 'Clear input form for further input.'),
        206: ('Partial Content', 'Partial content follows.'),

        300: ('Multiple Choices',
              'Object has several resources -- see URI list'),
        301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
        302: ('Found', 'Object moved temporarily -- see URI list'),
        303: ('See Other', 'Object moved -- see Method and URL list'),
        304: ('Not Modified',
              'Document has not changed since given time'),
        305: ('Use Proxy',
              'You must use proxy specified in Location to access this '
              'resource.'),
        307: ('Temporary Redirect',
              'Object moved temporarily -- see URI list'),

        400: ('Bad Request',
              'Bad request syntax or unsupported method'),
        401: ('Unauthorized',
              'No permission -- see authorization schemes'),
        402: ('Payment Required',
              'No payment -- see charging schemes'),
        403: ('Forbidden',
              'Request forbidden -- authorization will not help'),
        404: ('Not Found', 'Nothing matches the given URI'),
        405: ('Method Not Allowed',
              'Specified method is invalid for this resource.'),
        406: ('Not Acceptable', 'URI not available in preferred format.'),
        407: ('Proxy Authentication Required', 'You must authenticate with '
              'this proxy before proceeding.'),
        408: ('Request Timeout', 'Request timed out; try again later.'),
        409: ('Conflict', 'Request conflict.'),
        410: ('Gone',
              'URI no longer exists and has been permanently removed.'),
        411: ('Length Required', 'Client must specify Content-Length.'),
        412: ('Precondition Failed', 'Precondition in headers is false.'),
        413: ('Request Entity Too Large', 'Entity is too large.'),
        414: ('Request-URI Too Long', 'URI is too long.'),
        415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
        416: ('Requested Range Not Satisfiable',
              'Cannot satisfy request range.'),
        417: ('Expectation Failed',
              'Expect condition could not be satisfied.'),

        500: ('Internal Server Error', 'Server got itself in trouble'),
        501: ('Not Implemented',
              'Server does not support this operation'),
        502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
        503: ('Service Unavailable',
              'The server cannot process the request due to a high load'),
        504: ('Gateway Timeout',
              'The gateway server did not receive a timely response'),
        505: ('HTTP Version Not Supported', 'Cannot fulfill request.'),
        }


# ============ SocketServer.py ===========
class StreamRequestHandler(BaseRequestHandler):

    """Define self.rfile and self.wfile for stream sockets."""

    # Default buffer sizes for rfile, wfile.
    # We default rfile to buffered because otherwise it could be
    # really slow for large data (a getc() call per byte); we make
    # wfile unbuffered because (a) often after a write() we want to
    # read and we need to flush the line; (b) big writes to unbuffered
    # files are typically optimized by stdio even when big reads
    # aren't.
    rbufsize = -1
    wbufsize = 0

    # A timeout to apply to the request socket, if not None.
    timeout = None

    # Disable nagle algorithm for this socket, if True.
    # Use only when wbufsize != 0, to avoid small packets.
    disable_nagle_algorithm = False

    def setup(self):
        self.connection = self.request
        if self.timeout is not None:
            self.connection.settimeout(self.timeout)
        if self.disable_nagle_algorithm:
            self.connection.setsockopt(socket.IPPROTO_TCP,
                                       socket.TCP_NODELAY, True)
        self.rfile = self.connection.makefile('rb', self.rbufsize)
        self.wfile = self.connection.makefile('wb', self.wbufsize)

    def finish(self):
        if not self.wfile.closed:
            try:
                self.wfile.flush()
            except socket.error:
                # A final socket error may have occurred here, such as
                # the local error ECONNABORTED.
                pass
        self.wfile.close()
        self.rfile.close()


class BaseRequestHandler:

    """Base class for request handler classes.

    This class is instantiated for each request to be handled.  The
    constructor sets the instance variables request, client_address
    and server, and then calls the handle() method.  To implement a
    specific service, all you need to do is to derive a class which
    defines a handle() method.

    The handle() method can find the request as self.request, the
    client address as self.client_address, and the server (in case it
    needs access to per-server information) as self.server.  Since a
    separate instance is created for each request, the handle() method
    can define other arbitrary instance variables.

    """

    def __init__(self, request, client_address, server):
        self.request = request
        self.client_address = client_address
        self.server = server
        self.setup()
        try:
            self.handle()
        finally:
            self.finish()

    def setup(self):
        pass

    def handle(self):
        pass

    def finish(self):
        pass
