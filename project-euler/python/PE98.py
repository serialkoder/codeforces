import sys


def transforToNum(s):
    x = set(s)
    print(x)


words = sys.stdin.readline().strip().replace('"', "").split(",")
for w in words:
    transforToNum(w)
