import random

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

count = 0
i = 2
while count < 6:
    if isprime(i):
        count += 1
    i+=1

print(i-1)
