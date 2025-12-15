#!/usr/bin/env python3
# Contest: 1791  Problem: D - Distinct Split
# URL: https://codeforces.com/contest/1791/problem/D

import sys

t = int(sys.stdin.readline().strip())
for _ in range(0, t):
    n = int(sys.stdin.readline().strip())
    s = sys.stdin.readline().strip()
    prefix = [0] * (n + 1)
    suffix = [0] * (n + 2)
    unique = set()
    ind = 1
    for i in s:
        unique.add(i)
        prefix[ind] = len(unique)
        ind += 1
    ind = n
    unique = set()
    for i in reversed(s):
        unique.add(i)
        suffix[ind] = len(unique)
        ind -= 1
    ans = 0
    for i in range(1, n + 1):
        ans = max(ans, prefix[i] + suffix[i + 1])
    print(ans)
