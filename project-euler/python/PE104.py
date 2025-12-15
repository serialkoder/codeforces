import sys
import math

# Precompute constants for speed
LOG10_PHI = math.log10((1 + math.sqrt(5)) / 2.0)
LOG10_SQRT5 = 0.5 * math.log10(5)


def fib_first10(n: int) -> int:
    """
    First 10 digits of F_n via Binet/logs (approx but very reliable in practice).
    Returns an int in [1_000_000_000, 9_999_999_999] for n large enough.
    For small n where F_n has <10 digits, this returns that exact number.
    """
    if n == 0:
        return 0
    # log10(F_n) ≈ n*log10(phi) - log10(sqrt(5))
    x = n * LOG10_PHI - LOG10_SQRT5
    frac = x - math.floor(x)
    # First 10 digits = floor(10^(frac + 9))
    leading = int(10 ** (frac + 9) + 1e-12)  # epsilon fights float edge cases
    # Clamp in case rounding nudges to 10^10
    return leading if leading < 10_000_000_000 else 9_999_999_999


DIGITS_1_9 = frozenset("123456789")
sys.set_int_max_str_digits(1000000)


def isPandigital(N):
    cur = set(N)
    return len(cur) == 9 and cur == DIGITS_1_9


def isLeftPandigital(N):
    s = str(N)[0:9]
    return isPandigital(s)


def isRightPandigital(N):
    s = str(N)[-9:]
    return isPandigital(s)


M = 10**10  # modulus for "last 10 digits"


def _mat_mul(a, b):
    """Multiply 2x2 matrices a and b modulo M.
    Each matrix is a 4-tuple (a,b,c,d) representing [[a,b],[c,d]]."""
    a00, a01, a10, a11 = a
    b00, b01, b10, b11 = b
    return (
        (a00 * b00 + a01 * b10) % M,
        (a00 * b01 + a01 * b11) % M,
        (a10 * b00 + a11 * b10) % M,
        (a10 * b01 + a11 * b11) % M,
    )


def _mat_pow(n):
    """Compute [[1,1],[1,0]]^n modulo M via exponentiation by squaring."""
    base = (1, 1, 1, 0)  # Fibonacci Q-matrix
    res = (1, 0, 0, 1)  # identity
    while n > 0:
        if n & 1:
            res = _mat_mul(res, base)
        base = _mat_mul(base, base)
        n >>= 1
    return res  # [[F_{n+1}, F_n],[F_n, F_{n-1}]]


def fib_last10(n: int) -> int:
    """Return F_n modulo 10^10 (i.e., last 10 digits as an int)."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0
    a00, a01, a10, a11 = _mat_pow(n)
    return a01  # F_n


def fib_last10_str(n: int) -> str:
    """Return F_n as a zero-padded 10-digit string of its last 10 digits."""
    return str(fib_last10(n)).zfill(10)


for i in range(1, 1000000):
    y = fib_first10(i)
    if isLeftPandigital(y):
        x = fib_last10_str(i)
        if isRightPandigital(x):
            print(i, y, x)
