chain_counts = {1: 1}

def sequence_chain_counter(n):
    original_n = n  # Store original value
    count = 0
    while n not in chain_counts:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        count += 1

    # Memoize result
    chain_counts[original_n] = chain_counts[n] + count
    return chain_counts[original_n]

max_count = 0
ans = 0

for i in range(1, 1000000):
    cur = sequence_chain_counter(i)
    if cur > max_count:
        max_count = cur
        ans = i

print(ans, max_count)
