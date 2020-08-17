import socket
import time
import tcp_util
import io

tcp_util.new_ns()

ip = '127.0.0.1'
port = 20000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
if True:
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_USER_TIMEOUT, 5*1000)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 1) # two probes
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 1) # seconds
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 1) # seconds
s.bind((ip, port))
s.listen(16)

tcp_util.tcpdump_start(port)
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

tcp_util.drop_start(sport=port)


# setblocking 설정을 해주지 않으면 syn+ack 을 받지 못한 c socket 이 6번 재시도를 하게 된다
# 한번의 요청에 대한 syn+ack 재시도 횟수를 보기 위해서는 한번 시도 후 재시도 전에 socket close 를 해야 한다

c.setblocking(False)
try:
    c.connect((ip, port))
except io.BlockingIOError:
    pass

c.setblocking(True)
c.close()

while True:
    tcp_util.ss(port)
    time.sleep(2)

