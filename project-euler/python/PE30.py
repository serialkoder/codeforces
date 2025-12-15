i = 10
ans = 0
while  i < (9**5)*7:
	s = sum(int(x)**5 for x in str(i))
	if s == i:
		ans += i
	i += 1
print(ans)
