import argparse
from data import TraceResult
from dns import resolve
import route

def prepare_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("dst")
    parser.add_argument("-6", action="store_true", help="use IPv6 instead of IPv4")
    parser.add_argument("-u", action="store_true", help="use UDP instead of ICMP")
    parser.add_argument("-T", action="store_true", help="use TCP instead of ICMP")
    parser.add_argument("-P", action="store", default=80, type=int, help="port to use for UDP or TCP segments")
    args = parser.parse_args()

    l4 = "ICMP"
    if args.u:
        l4 = "UDP"
    if args.T:
        l4 = "TCP"
    return args.dst, args.__dict__["6"], l4, args.P

if __name__ == "__main__":
    addr, ipv6, l4, port = prepare_args()
    dstaddr = resolve(addr, ipv6)

    traceResult = TraceResult()
    while True:
        x = route.gather_route(dstaddr, ipv6, l4, port)
        traceResult.merge(x)
        print(traceResult)
