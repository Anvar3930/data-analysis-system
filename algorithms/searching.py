from typing import List, Any

def linear_search(a: List[Any], x: Any) -> int:
    for i, v in enumerate(a):
        if v == x:
            return i
    return -1

def binary_search(sorted_a: List[Any], x: Any) -> int:
    lo, hi = 0, len(sorted_a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sorted_a[mid] == x:
            return mid
        if sorted_a[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
