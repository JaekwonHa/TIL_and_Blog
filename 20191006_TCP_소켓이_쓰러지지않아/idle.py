import socket
import time

import select

import tcp_util
import sys

DEBUG = False
if len(sys.argv) != 1:
    DEBUG = sys.argv[1]

tcp_util.new_ns()

ip = '127.0.0.1'
port = 20000

tcp_util.tcpdump_start(port)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
s.bind((ip, port))
s.listen(16)

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
c.connect((ip, port))

if DEBUG:
    # c.setsockopt(socket.IPPROTO_TCP, socket.TCP_USER_TIMEOUT, 20000)
    c.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    c.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 3)  # seconds
    c.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 3)  # seconds
    c.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)

t0 = time.time()

tcp_util.drop_start(dport=port)
tcp_util.drop_start(sport=port)

time.sleep(2)
tcp_util.ss(port)

poll = select.poll()
poll.register(c, select.POLLIN)
poll.poll()

tcp_util.ss(port)

e = c.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
print("[ ] SO_ERROR = %s" % (e,))

t1 = time.time()
print("[ ] took: %f seconds" % (t1 - t0))
