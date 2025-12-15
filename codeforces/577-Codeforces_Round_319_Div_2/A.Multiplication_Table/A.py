#!/usr/bin/env python3
# Contest: 577  Problem: A - Multiplication Table
# URL: https://codeforces.com/contest/577/problem/A

import sys, math

n, x = map(int, sys.stdin.readline().strip().split())

seen = set()
ans = 0
for i in range(1, int(math.isqrt(x)) + 1):
    if x % i == 0:
        if (i, x // i) in seen:
            continue
        if i <= n and x / i <= n:
            ans += 1
            if i != x / i:
                ans += 1
            seen.add((i, x // i))
print(ans)
