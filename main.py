import csv
from typing import List, Dict, Any, Tuple

from models import Record

from storage.linear import DynamicArray, Stack, Queue, Deque, CircularList
from storage.associative import HashTableOpenAddressing, HashTableChaining
from storage.trees import BST, AVL, RedBlackTree, Trie, MinHeap, MaxHeap
from storage.specialized import DSU, BloomFilter, SegmentTree, Fenwick
from storage.graphs import GraphList, DirectedGraph, WeightedGraph

from algorithms.sorting import (
    bubble_sort, selection_sort, insertion_sort, merge_sort,
    quick_sort, heap_sort, counting_sort, radix_sort
)
from algorithms.searching import linear_search, binary_search
from algorithms.graphs import (
    dfs, bfs, dijkstra, bellman_ford, floyd_warshall,
    topological_sort, prim_mst, kruskal_mst
)
from algorithms.dp_greedy import factorial, divide_and_conquer_max, greedy_activity_selection, knapsack_01


def load_csv(path: str) -> List[Record]:
    out = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            out.append(Record(int(row["id"]), row["category"], int(row["value"]), row["text"]))
    return out


class DataAnalysisSystem:
    def __init__(self):
        self.records = DynamicArray()
        self.by_id: Dict[int, Record] = {}
        self.categories = set()

        self.ht_open = HashTableOpenAddressing()
        self.ht_chain = HashTableChaining()

        self.undo = Stack()
        self.events = Queue()
        self.window = Deque()
        self.recent = CircularList(capacity=5)

        self.bst = BST()
        self.avl = AVL()
        self.rbt = RedBlackTree()
        self.trie = Trie()
        self.bloom = BloomFilter(m=2048, k=4)

        self.minh = MinHeap()
        self.maxh = MaxHeap()

    def add_record(self, r: Record) -> None:
        if r.id in self.by_id:
            raise ValueError(f"id={r.id} already exists")
        self.records.append(r)
        self.by_id[r.id] = r
        self.categories.add(r.category)

        self.ht_open.put(r.id, r)
        self.ht_chain.put(r.id, r)

        self.bst.insert(r.value)
        self.avl.insert(r.value)
        self.rbt.insert(r.value)

        self.trie.insert(r.text)
        self.bloom.add(r.text)

        self.minh.push(r.value)
        self.maxh.push(r.value)

        self.undo.push(("remove", r.id))
        self.events.enqueue(("add", r.id))

        self.window.push_back(r.id)
        if len(self.window) > 5:
            self.window.pop_front()

        self.recent.add(r.id)

    def remove_record(self, record_id: int) -> None:
        if record_id not in self.by_id:
            raise KeyError(f"id={record_id} not found")
        r = self.by_id[record_id]
        del self.by_id[record_id]

        new_list = [x for x in self.records.to_list() if x.id != record_id]
        self.records = DynamicArray()
        for x in new_list:
            self.records.append(x)

        self.undo.push(("add", r))
        self.events.enqueue(("remove", record_id))

    def values(self) -> List[int]:
        return [rec.value for rec in self.records.to_list()]

    def texts(self) -> List[str]:
        return [rec.text for rec in self.records.to_list()]

    def demo_search(self) -> None:
        vals = self.values()
        print("\n=== SEARCH ===")
        print("Linear search value=150 idx:", linear_search(vals, 150))
        sorted_vals = merge_sort(vals)
        print("Binary search value=150 idx:", binary_search(sorted_vals, 150), "in", sorted_vals)
        print("Hash(Open) get id=4:", self.ht_open.get(4))
        print("Hash(Chain) get id=4:", self.ht_chain.get(4))

    def demo_sorting(self) -> None:
        vals = self.values()
        print("\n=== SORTING ===")
        print("Values:", vals)
        print("Bubble:", bubble_sort(vals))
        print("Selection:", selection_sort(vals))
        print("Insertion:", insertion_sort(vals))
        print("Merge:", merge_sort(vals))
        print("Quick:", quick_sort(vals))
        print("Heap:", heap_sort(vals))
        print("Counting:", counting_sort(vals))
        try:
            print("Radix:", radix_sort(vals))
        except Exception as e:
            print("Radix ERROR:", e)

    def demo_trees_indexing(self) -> None:
        print("\n=== TREES / INDEXING ===")
        print("BST inorder:", self.bst.inorder_list())
        print("AVL inorder:", self.avl.inorder_list())
        print("RBT inorder:", self.rbt.inorder_list())
        print("Trie prefix 'c':", self.trie.starts_with("c"))
        print("Bloom(cpu):", self.bloom.might_contain("cpu"))
        print("Bloom(unknown):", self.bloom.might_contain("unknown"))

    def demo_heaps(self) -> None:
        print("\n=== HEAPS ===")
        print("MinHeap peek:", self.minh.peek())
        print("MaxHeap peek:", self.maxh.peek())

    def demo_segment_fenwick(self) -> None:
        print("\n=== RANGE SUM (SEGMENT/FENWICK) ===")
        vals = self.values()
        st = SegmentTree(vals)
        fw = Fenwick(len(vals))
        for i, v in enumerate(vals):
            fw.add(i, v)
        r = min(3, len(vals) - 1)
        print("Segment sum(1..r):", st.query_sum(1, r))
        print("Fenwick sum(1..r):", fw.sum_range(1, r))

    def demo_graphs(self) -> None:
        print("\n=== GRAPHS ===")
        recs = self.records.to_list()
        if len(recs) < 2:
            print("Not enough records for graph demo")
            return

        g = GraphList()
        dg = DirectedGraph()
        wg = WeightedGraph()

        for i in range(len(recs) - 1):
            a = recs[i].category
            b = recs[i + 1].category
            g.add_edge(a, b)
            dg.add_edge(a, b)
            wg.add_edge(a, b, abs(recs[i].value - recs[i + 1].value))

        start = recs[0].category
        print("BFS:", bfs(g.adj, start))
        print("DFS:", dfs(g.adj, start))
        print("Dijkstra:", dijkstra(wg.adj, start))

        vertices = list(wg.adj.keys())
        edges = []
        for u in wg.adj:
            for v, w in wg.adj[u]:
                edges.append((u, v, w))

        print("Bellman-Ford:", bellman_ford(edges, vertices, start))

        wmap = {}
        for u, v, w in edges:
            wmap[(u, v)] = min(wmap.get((u, v), 10**9), w)
        dist_all = floyd_warshall(vertices, wmap)
        if vertices:
            print("Floyd sample:", (vertices[0], vertices[-1]), "=", dist_all[(vertices[0], vertices[-1])])

        print("Topo (by categories order edges):", topological_sort(dg.adj))

        if vertices:
            total_p, mst_p = prim_mst(wg.adj, vertices[0])
            print("Prim MST total:", total_p, "edges:", mst_p)
            total_k, mst_k = kruskal_mst(vertices, edges)
            print("Kruskal MST total:", total_k, "edges:", mst_k)

    def demo_dsu(self) -> None:
        print("\n=== DSU (Union-Find) ===")
        cats = sorted(list(self.categories))
        idx = {c: i for i, c in enumerate(cats)}
        dsu = DSU(len(cats))
        recs = self.records.to_list()
        for i in range(len(recs) - 1):
            dsu.union(idx[recs[i].category], idx[recs[i+1].category])
        groups: Dict[int, List[str]] = {}
        for c in cats:
            root = dsu.find(idx[c])
            groups.setdefault(root, []).append(c)
        print("Category groups:", list(groups.values()))

    def demo_dp_greedy(self) -> None:
        print("\n=== DP / GREEDY / RECURSION / D&C ===")
        print("factorial(6):", factorial(6))
        vals = self.values()
        print("divide&conquer max:", divide_and_conquer_max(vals))
        intervals = [(1,3),(2,5),(4,7),(6,9),(8,10)]
        print("greedy activities:", greedy_activity_selection(intervals))
        w = [2,3,4,5]
        v = [3,4,5,6]
        print("knapsack W=5:", knapsack_01(w, v, 5))


def main():
    sys = DataAnalysisSystem()

    data = load_csv("demo/sample_data.csv")
    for r in data:
        sys.add_record(r)

    print("Loaded records:", len(sys.records))
    print("Recent (circular):", sys.recent.to_list())
    print("Window (deque):", sys.window.to_list())

    sys.demo_search()
    sys.demo_sorting()
    sys.demo_trees_indexing()
    sys.demo_heaps()
    sys.demo_segment_fenwick()
    sys.demo_graphs()
    sys.demo_dsu()
    sys.demo_dp_greedy()

    print("\n=== REMOVE / UNDO STACK DEMO ===")
    sys.remove_record(3)
    print("After remove id=3 -> count:", len(sys.records))
    print("Undo top:", sys.undo.peek())
    print("Events queue len:", len(sys.events))

if __name__ == "__main__":
    main()
