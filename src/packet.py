import scapy.all as sc

class Packet:
    def __init__(self, dst, isv6, l4, port, ttl) -> None:
        self.ttl = ttl
        self.dst = dst
        self.l4 = l4
        l3 = self.prepare_l3(isv6)
        l4 = self.prepare_l4(isv6, port)
        self.sr(l3, l4)

    def prepare_l3(self, isv6):
        if isv6:
            return sc.IPv6(dst=self.dst, hlim=self.ttl)
        return sc.IP(dst=self.dst, ttl=self.ttl)

    def prepare_l4(self, isv6, port):
        if self.l4 == "ICMP":
            if isv6:
                return sc.ICMPv6EchoRequest()
            return sc.ICMP()
        elif self.l4 == "UDP":
            return sc.UDP(dport=port)
        elif self.l4 == "TCP":
            return sc.TCP(flags="S", dport=port)

    def sr(self, l3, l4):
        p = l3/l4
        self.res = sc.sr1(p, timeout=1, verbose=0)

    def is_timeout(self):
        return self.res is None

    def reached(self):
        return self.res.src == self.dst

    def addr(self):
        return self.res.src
