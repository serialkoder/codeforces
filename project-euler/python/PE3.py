def factorint(n):
	res = []
	i = 2
	while  i*i <= n:
		if n%i == 0:
			res.append(i)
			while n%i==0:
				n//=i;
		i += 1
	if n>1:
		res.append(n)
	return res
	

print(max(factorint(600851475143)))