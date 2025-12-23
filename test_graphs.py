from storage.graphs import GraphMatrix, GraphList, DirectedGraph, WeightedGraph
from algorithms.graphs import (
    dfs, bfs, dijkstra,
    bellman_ford, floyd_warshall,
    topological_sort, prim_mst, kruskal_mst
)

def main():
    verts = ["A", "B", "C", "D"]

    gm = GraphMatrix(verts)
    gm.add_edge("A", "B")
    gm.add_edge("B", "C")
    print("AdjMatrix A row:", gm.mat[gm.idx["A"]])

    gl = GraphList()
    gl.add_edge("A", "B")
    gl.add_edge("B", "C")
    gl.add_edge("A", "D")
    print("BFS:", bfs(gl.adj, "A"))
    print("DFS:", dfs(gl.adj, "A"))

    dg = DirectedGraph()
    dg.add_edge("A", "B")
    dg.add_edge("A", "C")
    dg.add_edge("B", "D")
    dg.add_edge("C", "D")
    print("Topo:", topological_sort(dg.adj))

    wg = WeightedGraph()
    wg.add_edge("A", "B", 4)
    wg.add_edge("A", "C", 2)
    wg.add_edge("C", "B", 1)
    wg.add_edge("B", "D", 5)
    wg.add_edge("C", "D", 8)

    print("Dijkstra from A:", dijkstra(wg.adj, "A"))

    vertices = list(wg.adj.keys())
    edges = []
    for u in wg.adj:
        for v, w in wg.adj[u]:
            edges.append((u, v, w))

    print("Bellman-Ford from A:", bellman_ford(edges, vertices, "A"))

    wmap = {}
    for u, v, w in edges:
        wmap[(u, v)] = min(wmap.get((u, v), 10**9), w)

    dist_all = floyd_warshall(vertices, wmap)
    print("Floyd A->D:", dist_all[("A", "D")])

    total_p, mst_p = prim_mst(wg.adj, "A")
    print("Prim MST total:", total_p, "edges:", mst_p)

    total_k, mst_k = kruskal_mst(vertices, edges)
    print("Kruskal MST total:", total_k, "edges:", mst_k)

if __name__ == "__main__":
    main()
