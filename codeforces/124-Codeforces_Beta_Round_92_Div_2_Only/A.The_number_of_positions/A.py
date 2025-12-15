#!/usr/bin/env python3
# Contest: 124  Problem: A - The number of positions
# URL: https://codeforces.com/contest/124/problem/A

import sys

data = sys.stdin.buffer.read().split()
it = iter(data)


def solve():
    n = int(next(it))
    a = int(next(it))
    b = int(next(it))
    ans = 0
    for i in range(n):
        ans += (1 if i >= a and n - i - 1 <= b else 0)
    print(ans)

if __name__ == "__main__":
    solve()
