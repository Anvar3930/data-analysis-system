from storage.specialized import DSU, BloomFilter, SegmentTree, Fenwick

def main():
    dsu = DSU(5)
    dsu.union(0, 1)
    dsu.union(3, 4)
    print("DSU same(0,1):", dsu.find(0) == dsu.find(1))
    print("DSU same(1,2):", dsu.find(1) == dsu.find(2))
    dsu.union(1, 2)
    print("DSU same(1,2) after union:", dsu.find(1) == dsu.find(2))

    bf = BloomFilter(m=512, k=3)
    bf.add("cpu")
    bf.add("case")
    print("Bloom cpu:", bf.might_contain("cpu"))
    print("Bloom iphone:", bf.might_contain("iphone"))

    a = [5, 80, 120, 7, 11]
    st = SegmentTree(a)
    print("Segment sum(1..3):", st.query_sum(1, 3))

    fw = Fenwick(len(a))
    for i, v in enumerate(a):
        fw.add(i, v)
    print("Fenwick sum(1..3):", fw.sum_range(1, 3))

if __name__ == "__main__":
    main()
