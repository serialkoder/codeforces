#!/usr/bin/env python3
# Contest: 1364  Problem: A - XXXXX
# URL: https://codeforces.com/contest/1364/problem/A

import sys
data = sys.stdin.buffer.read().decode("utf-8", errors="ignore").split()
it = iter(data)

def y():
    print("YES")

def n():
    print("NO")

def yn(ok: bool):
    print("YES" if ok else "NO")

def solve():
    # t = int(next(it))  # uncomment if multiple test cases
    # for _ in range(t):
    #     n = int(next(it))
    #     # arr = [int(next(it)) for __ in range(n)]
    #     # TODO: solve
    #     # print(answer)
    pass

if __name__ == "__main__":
    solve()
