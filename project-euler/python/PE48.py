ans = 0
for i in range(1,1001):
	# Since all mutliples of 2 & 5 are raised to exp more than 10 its okay to take 0 as sum for them
	ans += pow(i,i,10**10)

print(ans%10**10)