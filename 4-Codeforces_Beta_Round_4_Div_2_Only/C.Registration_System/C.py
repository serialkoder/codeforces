import sys
from collections import defaultdict

n = int(sys.stdin.readline().strip())
names = defaultdict(int)
for _ in range(n):
    cur = sys.stdin.readline().strip()
    count = names[cur]
    if count == 0:
        print("OK")
    else:
        print(cur + str((count)))
    names[cur] = count + 1
