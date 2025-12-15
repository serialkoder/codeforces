import math

def simple_sieve(limit):
    prime = [True] * (limit + 1)
    prime[0] = prime[1] = False
    for i in range(2, int(math.sqrt(limit)) + 1):
        if prime[i]:
            for j in range(i*i, limit + 1, i):
                prime[j] = False
    return [i for i, is_prime in enumerate(prime) if is_prime]

def segmented_sieve(L, R):
    limit = int(math.sqrt(R)) + 1
    primes = simple_sieve(limit)

    is_prime = [True] * (R - L + 1)

    for p in primes:
        start = max(p * p, ((L + p - 1) // p) * p)
        for j in range(start, R + 1, p):
            is_prime[j - L] = False

    if L == 1:
        is_prime[0] = False

    return [L + i for i, val in enumerate(is_prime) if val]

primes_in_range = segmented_sieve(10**9, 10**10)
print(len(primes_in_range))