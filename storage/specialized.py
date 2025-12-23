from typing import List
import hashlib

class DSU:
    def __init__(self, n: int):
        self.p = list(range(n))
        self.r = [0] * n

    def find(self, x: int) -> int:
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])
        return self.p[x]

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb: return False
        if self.r[ra] < self.r[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra
        if self.r[ra] == self.r[rb]:
            self.r[ra] += 1
        return True

class BloomFilter:
    def __init__(self, m: int = 1024, k: int = 3):
        self.m = m
        self.k = k
        self.bits = [0] * m

    def _hashes(self, s: str):
        for i in range(self.k):
            h = hashlib.sha256((str(i) + s).encode()).hexdigest()
            yield int(h, 16) % self.m

    def add(self, s: str) -> None:
        for h in self._hashes(s):
            self.bits[h] = 1

    def might_contain(self, s: str) -> bool:
        return all(self.bits[h] == 1 for h in self._hashes(s))

class SegmentTree:
    def __init__(self, a: List[int]):
        self.n = len(a)
        self.t = [0] * (4 * self.n) if self.n else [0]
        if self.n:
            self._build(1, 0, self.n - 1, a)

    def _build(self, v: int, tl: int, tr: int, a: List[int]) -> None:
        if tl == tr:
            self.t[v] = a[tl]
            return
        tm = (tl + tr) // 2
        self._build(v*2, tl, tm, a)
        self._build(v*2+1, tm+1, tr, a)
        self.t[v] = self.t[v*2] + self.t[v*2+1]

    def query_sum(self, l: int, r: int) -> int:
        def _q(v: int, tl: int, tr: int, l: int, r: int) -> int:
            if l > r: return 0
            if l == tl and r == tr: return self.t[v]
            tm = (tl + tr) // 2
            return _q(v*2, tl, tm, l, min(r, tm)) + _q(v*2+1, tm+1, tr, max(l, tm+1), r)
        if not self.n: return 0
        return _q(1, 0, self.n - 1, l, r)

class Fenwick:
    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i: int, delta: int) -> None:
        i += 1
        while i <= self.n:
            self.bit[i] += delta
            i += i & -i

    def sum_prefix(self, i: int) -> int:
        i += 1
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

    def sum_range(self, l: int, r: int) -> int:
        return self.sum_prefix(r) - (self.sum_prefix(l - 1) if l > 0 else 0)
