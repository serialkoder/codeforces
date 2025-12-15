#!/usr/bin/env python3
# Contest: 499  Problem: B - Lecture
# URL: https://codeforces.com/contest/499/problem/B

import sys

n, m = map(int, sys.stdin.readline().strip().split())
words = {}
for _ in range(0, m):
    x, y = sys.stdin.readline().strip().split()
    words[x] = y
lecture = sys.stdin.readline().strip().split()

for w in lecture:
    if len(words[w]) < len(w):
        sys.stdout.write(words[w] + " ")
    else:
        sys.stdout.write(w + " ")
print("")
