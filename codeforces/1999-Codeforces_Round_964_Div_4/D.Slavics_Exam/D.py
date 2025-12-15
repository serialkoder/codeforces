#!/usr/bin/env python3
# Contest: 1999  Problem: D - Slavic's Exam
# URL: https://codeforces.com/contest/1999/problem/D

import sys

data = sys.stdin.buffer.read().decode().split()
it = iter(data)


def solve():
    t = int(next(it))  # uncomment if multiple test cases
    for _ in range(t):
        s = next(it)
        t = next(it)
        res = list(s)
        j = 0
        for i in range(len(res)):
            ch = res[i]
            if j < len(t) and (t[j] == ch or ch == '?'):
                if ch == '?':
                    res[i] = t[j]
                j += 1
        for i in range(len(res)):
            if res[i] == '?':
                res[i] = 'a'
        if j == len(t):
            print("YES")
            print(''.join(res))
        else:
            print("NO")


if __name__ == "__main__":
    solve()
