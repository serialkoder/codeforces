def pell_negative_solutions():
    # Start with the smallest non-trivial solution (X, Y) for X^2 - 2Y^2 = -1
    X, Y = 1, 1

    while True:
        # Convert back to n, b, r
        n = (X + 1) // 2
        b = (Y + 1) // 2
        r = n - b
        if n > 1000000000000:
            print(n, r, b)
            break
        # Apply recurrence: multiply by (3 + 2√2)
        X, Y = 3 * X + 4 * Y, 2 * X + 3 * Y


# Example: first 6 solutions
print(pell_negative_solutions())
