from typing import Any, Dict, List, Tuple

class GraphMatrix:
    def __init__(self, vertices: List[Any]):
        self.vertices = vertices[:]
        self.idx = {v: i for i, v in enumerate(vertices)}
        n = len(vertices)
        self.mat = [[0] * n for _ in range(n)]

    def add_edge(self, u: Any, v: Any) -> None:
        i, j = self.idx[u], self.idx[v]
        self.mat[i][j] = 1
        self.mat[j][i] = 1

class GraphList:
    def __init__(self):
        self.adj: Dict[Any, List[Any]] = {}

    def add_edge(self, u: Any, v: Any) -> None:
        self.adj.setdefault(u, []).append(v)
        self.adj.setdefault(v, []).append(u)

class DirectedGraph:
    def __init__(self):
        self.adj: Dict[Any, List[Any]] = {}

    def add_edge(self, u: Any, v: Any) -> None:
        self.adj.setdefault(u, []).append(v)
        self.adj.setdefault(v, [])

class WeightedGraph:
    def __init__(self):
        self.adj: Dict[Any, List[Tuple[Any, int]]] = {}

    def add_edge(self, u: Any, v: Any, w: int) -> None:
        self.adj.setdefault(u, []).append((v, w))
        self.adj.setdefault(v, []).append((u, w))
