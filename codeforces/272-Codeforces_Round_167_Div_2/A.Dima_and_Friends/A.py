#!/usr/bin/env python3
# Contest: 272  Problem: A - Dima and Friends
# URL: https://codeforces.com/contest/272/problem/A

import sys

data = sys.stdin.buffer.read().split()
it = iter(data)


def solve():
    n = int(next(it))
    finger_count = 0
    ans = 0
    for i in range(n):
        finger_count += int(next(it))

    for i in range(1, 6):
        if (finger_count + i) % (n + 1) != 1:
            ans += 1
    print(ans)


if __name__ == "__main__":
    solve()
