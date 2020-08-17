import socket
import time
import tcp_util
import sys
import io
import select

DEBUG = False
if len(sys.argv) != 1:
    DEBUG = sys.argv[1]

port = 20000

tcp_util.new_ns()

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
#c.setsockopt(socket.IPPROTO_TCP, socket.TCP_SYNCNT, 6)
c.setsockopt(socket.IPPROTO_TCP, socket.TCP_USER_TIMEOUT, 5*1000)

t0 = time.time()

tcp_util.drop_start(dport=port)
tcp_util.tcpdump_start(port)

if DEBUG:
    c.setblocking(False)
    try:
        c.connect(('127.0.0.1', port))
    except io.BlockingIOError:
        pass
    c.setblocking(True)

    tcp_util.ss(port)
    time.sleep(1)
    tcp_util.ss(port)
    time.sleep(3)
    tcp_util.ss(port)

    poll = select.poll()
    poll.register(c, select.POLLOUT)
    poll.poll()
    tcp_util.ss(port)
else:
    try:
        c.connect(('127.0.0.1', port))
    except Exception as e:
        print(e)

e = c.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
print("[ ] SO_ERROR = %s" % (e,))

t1 = time.time()
