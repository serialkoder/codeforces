import random


def sum_of_primes(n):
    sieve = [True] * (n+1)
    sieve[0] = sieve[1] = False
    for i in range(2,int(n**0.5)+1):
        if sieve[i]:
            for j in range(i*i,n+1,i):
                sieve[j] = False
    return sum(i for i in range(n+1) if sieve[i])

def isprime(n, k=5):  # k = number of iterations
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # Write n-1 as d * 2^r
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1

    # Perform Miller-Rabin test k times
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)  # Compute a^d % n

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False  # Composite number found

    return True

# ans = 0
# for i in range(1,2000000):
#     if isprime(i):
#         ans += i

print(sum_of_primes(2000000))