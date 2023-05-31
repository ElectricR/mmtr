import scapy.all as sc

def resolve(addr, isv6):
    if isv6:
        res = sc.sr1(sc.IP(dst="8.8.8.8")/sc.UDP(dport=53)/sc.DNS(rd=1, qd=sc.DNSQR(qname=addr, qtype="AAAA")), verbose=0)
    else:
        res = sc.sr1(sc.IP(dst="8.8.8.8")/sc.UDP(dport=53)/sc.DNS(rd=1, qd=sc.DNSQR(qname=addr)), verbose=0)
    if not res.an:
        raise Exception("DNS query failed")
    return res.an.rdata
