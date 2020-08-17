import ctypes
import os
import subprocess
import sys

LIBC = ctypes.CDLL("libc.so.6")

tcpdump_bin = os.popen('which tcpdump').read().strip()
ss_bin = os.popen('which ss').read().strip()

CLONE_NEWNET = 0x40000000
original_net_ns = open("/proc/self/ns/net", 'rb')


def new_ns():
    r = LIBC.unshare(CLONE_NEWNET)
    if r != 0:
        print("[!] Are you root? Need unshare() syscall.")
        sys.exit(-1)
    os.system("ip link set lo up")


def tcpdump_start(port):
    # p = subprocess.Popen(('%s -B 16384 --packet-buffered -n -ttttt -i lo port %s -C 500 -w ./tcpdump.pcap' % (tcpdump_bin, port)).split())
    p = subprocess.Popen(('%s -B 16384 --packet-buffered -n -ttttt -i lo port %s' % (tcpdump_bin, port)).split())
    return p


def ss(port):
    print(os.popen('%s -t -n -o -a dport = :%s or sport = :%s' % (ss_bin, port, port)).read())


def do_iptables(action, sport, dport, extra):
    if sport:
        sport = '--sport %d' % (sport,)
        dport = ''
    else:
        sport = ''
        dport = '--dport %d' % (dport,)
    os.system("iptables -%s INPUT -i lo -p tcp %s %s %s -j DROP" % (action, sport, dport, extra))


def drop_start(sport=None, dport=None, extra=''):
    do_iptables('I', sport, dport, extra)


def drop_stop(sport=None, dport=None, extra=''):
    do_iptables('D', sport, dport, extra)
