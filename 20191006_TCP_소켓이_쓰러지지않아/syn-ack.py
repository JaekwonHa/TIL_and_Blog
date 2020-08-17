import socket
import time
import tcp_util
import io
import sys

DEBUG = False
if len(sys.argv) != 1:
    DEBUG = sys.argv[1]

tcp_util.new_ns()

ip = '127.0.0.1'
port = 20000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_DEFER_ACCEPT, 100)
if DEBUG:
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_USER_TIMEOUT, 5*1000)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 1) # two probes
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 1) # seconds
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 1) # seconds
s.bind((ip, port))
s.listen(16)

tcp_util.tcpdump_start(port)
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

t0 = time.time()

tcp_util.drop_stop(dport=port, extra='--tcp-flag SYN,ACK,FIN,RST,PSH ACK')

c.setblocking(False)
try:
    c.connect((ip, port))
except io.BlockingIOError:
    pass
c.setblocking(True)

tcp_util.ss(port)
time.sleep(2)
tcp_util.ss(port)
time.sleep(2)
tcp_util.ss(port)
time.sleep(2)
tcp_util.ss(port)
time.sleep(2)
tcp_util.ss(port)
print("[x] send")
c.send(b"hello world")
tcp_util.ss(port)
time.sleep(2)
tcp_util.ss(port)