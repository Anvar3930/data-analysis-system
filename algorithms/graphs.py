from typing import Any, Dict, List, Tuple, Set
import heapq

def dfs(adj: Dict[Any, List[Any]], start: Any) -> List[Any]:
    seen: Set[Any] = set()
    out: List[Any] = []
    def _go(u: Any):
        seen.add(u)
        out.append(u)
        for v in adj.get(u, []):
            if v not in seen:
                _go(v)
    _go(start)
    return out

def bfs(adj: Dict[Any, List[Any]], start: Any) -> List[Any]:
    seen = {start}
    q = [start]
    out = []
    i = 0
    while i < len(q):
        u = q[i]; i += 1
        out.append(u)
        for v in adj.get(u, []):
            if v not in seen:
                seen.add(v)
                q.append(v)
    return out

def dijkstra(adj: Dict[Any, List[Tuple[Any, int]]], start: Any) -> Dict[Any, int]:
    dist: Dict[Any, int] = {start: 0}
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist.get(u, 10**18):
            continue
        for v, w in adj.get(u, []):
            nd = d + w
            if nd < dist.get(v, 10**18):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist

def bellman_ford(edges: List[Tuple[Any, Any, int]], vertices: List[Any], start: Any) -> Dict[Any, int]:
    INF = 10**15
    dist = {v: INF for v in vertices}
    dist[start] = 0
    for _ in range(len(vertices) - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    return dist

def floyd_warshall(vertices: List[Any], wmap: Dict[Tuple[Any, Any], int]) -> Dict[Tuple[Any, Any], int]:
    INF = 10**12
    dist: Dict[Tuple[Any, Any], int] = {}
    for i in vertices:
        for j in vertices:
            if i == j:
                dist[(i, j)] = 0
            else:
                dist[(i, j)] = wmap.get((i, j), INF)
    for k in vertices:
        for i in vertices:
            dik = dist[(i, k)]
            if dik >= INF: 
                continue
            for j in vertices:
                nd = dik + dist[(k, j)]
                if nd < dist[(i, j)]:
                    dist[(i, j)] = nd
    return dist

def topological_sort(adj: Dict[Any, List[Any]]) -> List[Any]:
    indeg: Dict[Any, int] = {}
    for u in adj:
        indeg.setdefault(u, 0)
        for v in adj[u]:
            indeg[v] = indeg.get(v, 0) + 1
    q = [v for v in indeg if indeg[v] == 0]
    out = []
    i = 0
    while i < len(q):
        u = q[i]; i += 1
        out.append(u)
        for v in adj.get(u, []):
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return out

def prim_mst(adj: Dict[Any, List[Tuple[Any, int]]], start: Any):
    seen = {start}
    pq = []
    for v, w in adj.get(start, []):
        heapq.heappush(pq, (w, start, v))
    total = 0
    mst = []
    while pq:
        w, u, v = heapq.heappop(pq)
        if v in seen:
            continue
        seen.add(v)
        total += w
        mst.append((u, v, w))
        for to, wt in adj.get(v, []):
            if to not in seen:
                heapq.heappush(pq, (wt, v, to))
    return total, mst

def kruskal_mst(vertices: List[Any], edges: List[Tuple[Any, Any, int]]):
    parent = {v: v for v in vertices}
    rank = {v: 0 for v in vertices}

    def find(x: Any) -> Any:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: Any, b: Any) -> bool:
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        if rank[ra] < rank[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]:
            rank[ra] += 1
        return True

    edges2 = sorted(edges, key=lambda x: x[2])
    total = 0
    mst = []
    for u, v, w in edges2:
        if union(u, v):
            total += w
            mst.append((u, v, w))
    return total, mst
