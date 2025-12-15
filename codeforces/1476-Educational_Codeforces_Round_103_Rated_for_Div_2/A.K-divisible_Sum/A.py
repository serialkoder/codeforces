#!/usr/bin/env python3
# Contest: 1476  Problem: A - K-divisible Sum
# URL: https://codeforces.com/contest/1476/problem/A

import sys
import math

t = int(sys.stdin.readline().strip())
for _ in range(0, t):
    n, k = map(int, sys.stdin.readline().strip().split())
    if n <= k:
        print(math.ceil(k / n))
    else:
        a = math.ceil(n / k) * k
        print(math.ceil(a / n))
