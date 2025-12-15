def is_prime(n):
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in [2, 3, 5, 7, 11]:  # these bases are enough for n < 2^32
        if pow(a, d, n) == 1:
            continue
        for r in range(s):
            if pow(a, d * (2**r), n) == n - 1:
                break
        else:
            return False
    return True


def is_pair_prime(a, b):
    return is_prime(concat(a, b)) and is_prime(concat(b, a))


def concat(a, b):
    return int("".join([str(a), str(b)]))


LIM = 1000
sol = set()
for i in range(2, LIM):
    if is_prime(i):
        for j in range(i + 1, LIM):
            if is_prime(j) and is_pair_prime(i, j):
                sol.add((i, j))
sol1 = ()
for i in range(2, LIM * 3):
    if is_prime(i):
        for a, b in sol:
            if is_pair_prime(i, a) and is_pair_prime(i, b):
                sol1.add((i, a, b))
sol2 = []
for i in range(2, LIM * 3):
    if is_prime(i):
        for a, b, c in sol1:
            if is_pair_prime(i, a) and is_pair_prime(i, b) and is_pair_prime(i, c):
                sol2.append((i, a, b, c))
print(sol2)
sol3 = []
for i in range(2, LIM * 4):
    if is_prime(i):
        for a, b, c, d in sol2:
            if (
                is_pair_prime(i, a)
                and is_pair_prime(i, b)
                and is_pair_prime(i, c)
                and is_pair_prime(i, d)
            ):
                sol3.append((i, a, b, c, d))
print(sol3)
