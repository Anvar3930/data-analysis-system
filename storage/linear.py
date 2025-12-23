from typing import Any, Optional, List
from collections import deque

class Array:
    def __init__(self, size: int, fill: Any = None):
        self._data = [fill] * size
    def __len__(self): return len(self._data)
    def __getitem__(self, i: int): return self._data[i]
    def __setitem__(self, i: int, v: Any): self._data[i] = v
    def to_list(self) -> List[Any]: return list(self._data)

class DynamicArray:
    def __init__(self):
        self._data: List[Any] = []
    def append(self, x: Any) -> None: self._data.append(x)
    def pop(self) -> Any: return self._data.pop()
    def __len__(self): return len(self._data)
    def __getitem__(self, i: int): return self._data[i]
    def to_list(self) -> List[Any]: return list(self._data)

class SLLNode:
    def __init__(self, val: Any, nxt: Optional["SLLNode"] = None):
        self.val = val
        self.nxt = nxt

class SinglyLinkedList:
    def __init__(self):
        self.head: Optional[SLLNode] = None
    def push_front(self, x: Any) -> None:
        self.head = SLLNode(x, self.head)
    def to_list(self) -> List[Any]:
        out=[]
        cur=self.head
        while cur:
            out.append(cur.val)
            cur=cur.nxt
        return out

class DLLNode:
    def __init__(self, val: Any):
        self.val = val
        self.prev: Optional["DLLNode"] = None
        self.nxt: Optional["DLLNode"] = None

class DoublyLinkedList:
    def __init__(self):
        self.head: Optional[DLLNode] = None
        self.tail: Optional[DLLNode] = None
    def append(self, x: Any) -> None:
        node = DLLNode(x)
        if not self.tail:
            self.head = self.tail = node
            return
        self.tail.nxt = node
        node.prev = self.tail
        self.tail = node
    def to_list(self) -> List[Any]:
        out=[]
        cur=self.head
        while cur:
            out.append(cur.val)
            cur=cur.nxt
        return out

class CircularList:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.data = [None] * capacity
        self.i = 0
        self.count = 0
    def add(self, x: Any) -> None:
        self.data[self.i] = x
        self.i = (self.i + 1) % self.capacity
        self.count = min(self.count + 1, self.capacity)
    def to_list(self) -> List[Any]:
        if self.count < self.capacity:
            return self.data[:self.count]
        return self.data[self.i:] + self.data[:self.i]

class Stack:
    def __init__(self):
        self._a: List[Any] = []
    def push(self, x: Any) -> None: self._a.append(x)
    def pop(self) -> Any: return self._a.pop()
    def peek(self) -> Any: return self._a[-1]
    def __len__(self): return len(self._a)

class Queue:
    def __init__(self):
        self._q = deque()
    def enqueue(self, x: Any) -> None: self._q.append(x)
    def dequeue(self) -> Any: return self._q.popleft()
    def __len__(self): return len(self._q)

class Deque:
    def __init__(self):
        self._d = deque()
    def push_front(self, x: Any) -> None: self._d.appendleft(x)
    def push_back(self, x: Any) -> None: self._d.append(x)
    def pop_front(self) -> Any: return self._d.popleft()
    def pop_back(self) -> Any: return self._d.pop()
    def __len__(self): return len(self._d)
    def to_list(self) -> List[Any]: return list(self._d)
