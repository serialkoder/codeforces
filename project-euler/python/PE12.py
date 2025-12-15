def factorint(n):
	res = {}
	i = 2
	while  i*i <= n:
		count = 0
		if n%i == 0:			
			while n%i==0:
				n//=i;
				count += 1
			res[i]=count
		i += 1
	if n>1:
		res[n]=1

	return res

def count_divisors(n):
	factors = factorint(n)
	count =  1
	for x in factors.keys():
		count *= (factors[x]+1)
	return count

def triangular_number(n):
	return n*(n+1)//2

index = 1
while True:
	count = count_divisors(triangular_number(index))
	if count>=500:
		print(triangular_number(index))
		break
	index += 1