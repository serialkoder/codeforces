# Concise solver for D(n★, m) mod MOD.  Works when m | (MOD-1) and MOD is prime.
MOD = 999_999_001


# ---- tiny utils ----
def sieve(n):
    a = [True] * (n + 1)
    a[0] = a[1] = False
    for i in range(2, int(n**0.5) + 1):
        if a[i]:
            a[i * i : n + 1 : i] = [False] * (((n - i * i) // i) + 1)
    return [i for i, v in enumerate(a) if v]


def inv(x):
    return pow(x, MOD - 2, MOD)


def pfactors(n):
    f = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            f.append(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2  # try 2, then odds
    if n > 1:
        f.append(n)
    return f


def primitive_root(mod):
    phi = mod - 1
    fac = pfactors(phi)
    g = 2
    while True:
        if all(pow(g, phi // q, mod) != 1 for q in fac):
            return g
        g += 1


# Sum of triangular numbers along an arithmetic progression:
# S_tri(n, s) = sum_{k=1..K} T(n - s*k + 1), where K = n//s and T(x)=x(x+1)/2
def S_tri(n, s):
    K = n // s
    A = n + 1
    S1 = K * A - s * K * (K + 1) // 2  # sum m
    S2 = (
        K * A * A - s * A * K * (K + 1) + s * s * K * (K + 1) * (2 * K + 1) // 6
    )  # sum m^2
    return (S2 + S1) // 2


def D_superduper(n, m):
    # exponents in n★
    primes = sieve(n)
    exps = []
    for p in primes:
        e, s = 0, p
        while s <= n:
            e += S_tri(n, s)
            s *= p
        exps.append((p, e))

    # roots-of-unity filter
    zeta = pow(primitive_root(MOD), (MOD - 1) // m, MOD)
    t, total = 1, 0
    for _ in range(m):
        prod = 1
        for p, e in exps:
            r = (p * t) % MOD
            s = (
                (e + 1) % MOD
                if r == 1
                else (pow(r, e + 1, MOD) - 1) * inv((r - 1) % MOD) % MOD
            )
            prod = (prod * s) % MOD
        total = (total + prod) % MOD
        t = (t * zeta) % MOD
    return (total * inv(m)) % MOD


# --- answers ---
print(D_superduper(6, 6))  # -> 81625078  (that's D(6★,6) mod MOD)
print(D_superduper(1000, 1000))  # -> 882086212
