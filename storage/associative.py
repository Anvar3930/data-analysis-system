from typing import Any, List, Tuple

class HashTableOpenAddressing:
    def __init__(self, capacity: int = 101):
        self.cap = capacity
        self.keys = [None] * capacity
        self.vals = [None] * capacity
        self.size = 0

    def _hash(self, k: Any) -> int:
        return hash(k) % self.cap

    def put(self, k: Any, v: Any) -> None:
        i = self._hash(k)
        start = i
        while self.keys[i] is not None and self.keys[i] != k:
            i = (i + 1) % self.cap
            if i == start:
                raise RuntimeError("HashTable full")
        if self.keys[i] is None:
            self.size += 1
        self.keys[i] = k
        self.vals[i] = v

    def get(self, k: Any) -> Any:
        i = self._hash(k)
        start = i
        while self.keys[i] is not None:
            if self.keys[i] == k:
                return self.vals[i]
            i = (i + 1) % self.cap
            if i == start:
                break
        return None

class HashTableChaining:
    def __init__(self, capacity: int = 101):
        self.cap = capacity
        self.buckets: List[List[Tuple[Any, Any]]] = [[] for _ in range(capacity)]

    def _hash(self, k: Any) -> int:
        return hash(k) % self.cap

    def put(self, k: Any, v: Any) -> None:
        b = self.buckets[self._hash(k)]
        for i, (kk, _) in enumerate(b):
            if kk == k:
                b[i] = (k, v)
                return
        b.append((k, v))

    def get(self, k: Any) -> Any:
        b = self.buckets[self._hash(k)]
        for kk, vv in b:
            if kk == k:
                return vv
        return None
