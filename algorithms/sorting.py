from typing import List
import heapq

def bubble_sort(a: List[int]) -> List[int]:
    a = a[:]
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - 1 - i):
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                swapped = True
        if not swapped:
            break
    return a

def selection_sort(a: List[int]) -> List[int]:
    a = a[:]
    n = len(a)
    for i in range(n):
        mn = i
        for j in range(i+1, n):
            if a[j] < a[mn]:
                mn = j
        a[i], a[mn] = a[mn], a[i]
    return a

def insertion_sort(a: List[int]) -> List[int]:
    a = a[:]
    for i in range(1, len(a)):
        x = a[i]
        j = i - 1
        while j >= 0 and a[j] > x:
            a[j+1] = a[j]
            j -= 1
        a[j+1] = x
    return a

def merge_sort(a: List[int]) -> List[int]:
    if len(a) <= 1:
        return a[:]
    mid = len(a)//2
    L = merge_sort(a[:mid])
    R = merge_sort(a[mid:])
    i=j=0
    out=[]
    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            out.append(L[i]); i += 1
        else:
            out.append(R[j]); j += 1
    out.extend(L[i:])
    out.extend(R[j:])
    return out

def quick_sort(a: List[int]) -> List[int]:
    a = a[:]
    def _qs(lo: int, hi: int):
        if lo >= hi: return
        pivot = a[(lo+hi)//2]
        i, j = lo, hi
        while i <= j:
            while a[i] < pivot: i += 1
            while a[j] > pivot: j -= 1
            if i <= j:
                a[i], a[j] = a[j], a[i]
                i += 1; j -= 1
        _qs(lo, j)
        _qs(i, hi)
    if a:
        _qs(0, len(a)-1)
    return a

def heap_sort(a: List[int]) -> List[int]:
    h = a[:]
    heapq.heapify(h)
    out=[]
    while h:
        out.append(heapq.heappop(h))
    return out

def counting_sort(a: List[int]) -> List[int]:
    if not a: return []
    mn, mx = min(a), max(a)
    k = mx - mn + 1
    cnt = [0] * k
    for x in a:
        cnt[x - mn] += 1
    out=[]
    for i, c in enumerate(cnt):
        if c:
            out.extend([i + mn] * c)
    return out

def radix_sort(a: List[int]) -> List[int]:
    if not a: return []
    if any(x < 0 for x in a):
        raise ValueError("radix_sort supports only non-negative ints")
    out = a[:]
    exp = 1
    mx = max(out)
    while mx // exp > 0:
        buckets = [0]*10
        for x in out:
            buckets[(x//exp) % 10] += 1
        for i in range(1,10):
            buckets[i] += buckets[i-1]
        tmp = [0]*len(out)
        for i in range(len(out)-1, -1, -1):
            d = (out[i]//exp) % 10
            buckets[d] -= 1
            tmp[buckets[d]] = out[i]
        out = tmp
        exp *= 10
    return out
