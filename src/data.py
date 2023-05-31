import os

class TraceResult:
    def __init__(self) -> None:
        self.route = []
        self.iters = 1

    def empty(self):
        return len(self.route) == 0

    def merge(self, other):
        if self.empty():
            self.route = other.route.copy()
            self.iters = other.iters
        else:
            if len(self.route) != len(other.route):
                raise Exception(f"route has changed since the beginning of tracing: previous length is {len(self.route)}, current is {len(other.route)}")
            for i in range(len(other.route)):
                if self.route[i][0] == "***":
                    self.route[i][0] = other.route[i][0]
                    self.route[i][1] += other.route[i][1]
                elif other.route[i][0] == "***" or self.route[i][0] == other.route[i][0]:
                    self.route[i][1] += other.route[i][1]
                else:
                    raise Exception(f"route has changed since the beginning of tracing: previous addr is {self.route[i][0]}, current is {other.route[i][0]}")
            self.iters += other.iters

    def __str__(self):
        x = ""
        x += f"Traceroute iteration №{self.iters}{os.linesep}"
        for i in range(len(self.route)):
            x += f"\t{self.route[i][0]}: {self.route[i][1]/self.iters*100:.2f}%{os.linesep}"
        return x

    def add(self, addr, success):
        self.route.append([addr, success])
