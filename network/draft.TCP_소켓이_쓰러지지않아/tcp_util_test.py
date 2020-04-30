import tcp_util

port = 22

tcp_util.tcpdump_start(port)

tcp_util.ss(port)