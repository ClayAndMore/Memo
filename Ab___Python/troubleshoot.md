

### [python socket.error: [Errno 9\] Bad file descriptor]

The reason is that you are trying to reconnect a **closed** socket. You have to either create a new socket or reuse the old one as long as it's connected.

https://stackoverflow.com/questions/38292142/python-socket-error-errno-9-bad-file-descriptor

