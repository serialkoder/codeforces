def isPalindrome(n):
	a = str(n)
	b = str(n)[::-1]
	return a==b
ans = 0
for i in range(100,999):
	for j in range(100,999):
		num = i*j
		if isPalindrome(num):
			ans = max(ans,num)
print(ans)
