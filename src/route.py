from data import TraceResult
from packet import Packet

def gather_route(dst, isv6, l4, port, max_ttl=30):
    traceResult = TraceResult()
    for i in range(1, max_ttl+1):
        p = Packet(dst, isv6, l4, port, i)
        if p.is_timeout():
            traceResult.add(f"***", 0)
        else:
            traceResult.add(p.addr(), 1)
            if p.reached():
                break
    return traceResult
