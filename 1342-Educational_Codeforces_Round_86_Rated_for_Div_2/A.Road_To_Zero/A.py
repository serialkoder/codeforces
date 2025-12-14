import sys

t = int(sys.stdin.readline().strip())
for _ in range(0, t):
    x, y = map(int, sys.stdin.readline().strip().split())
    a, b = map(int, sys.stdin.readline().strip().split())
    r1 = (x + y) * a
    r2 = (max(x, y) - min(x, y)) * a + min(x, y) * b
    print(min(r1, r2))
