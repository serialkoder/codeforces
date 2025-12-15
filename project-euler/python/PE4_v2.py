def isPalindrome(n):
    a = str(n)
    b = str(n)[::-1]
    return a==b

ans = 0
for i in range(999, 99, -1):  # Start from 999 down to 100
    for j in range(i, 99, -1):  # Avoid duplicate pairs
        num = i * j
        if num <= ans:
            break  # No need to continue
        if isPalindrome(num):
            ans = max(ans, num)

print(ans)
