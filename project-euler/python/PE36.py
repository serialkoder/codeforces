def is_palin(n):
    rev = int("".join(reversed(str(n))))
    return n == rev


def is_palin_bin(n):
    rev = "".join(reversed(n))
    return n == rev


print(sum(i for i in range(1000000) if is_palin(i) and is_palin_bin(bin(i)[2:])))
