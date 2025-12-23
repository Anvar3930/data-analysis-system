from typing import List, Tuple

def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0")
    if n <= 1:
        return 1
    return n * factorial(n - 1)

def divide_and_conquer_max(a: List[int]) -> int:
    if not a:
        raise ValueError("empty list")
    def _max(l: int, r: int) -> int:
        if l == r:
            return a[l]
        m = (l + r) // 2
        left = _max(l, m)
        right = _max(m + 1, r)
        return left if left >= right else right
    return _max(0, len(a) - 1)

def greedy_activity_selection(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    intervals = sorted(intervals, key=lambda x: x[1])
    res = []
    last_end = -10**18
    for s, e in intervals:
        if s >= last_end:
            res.append((s, e))
            last_end = e
    return res

def knapsack_01(weights: List[int], values: List[int], W: int) -> int:
    n = len(weights)
    dp = [0] * (W + 1)
    for i in range(n):
        w, v = weights[i], values[i]
        for cap in range(W, w - 1, -1):
            dp[cap] = max(dp[cap], dp[cap - w] + v)
    return dp[W]
