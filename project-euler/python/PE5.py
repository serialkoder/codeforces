def merge_using_max(m1,m2):
	res = {}
	for x in m1.keys():
		if x in m2:
			res[x]=max(m1[x],m2[x])
		else:
			res[x]=m1[x]
	for x in m2.keys():
		if x in m1:
			res[x]=max(m1[x],m2[x])
		else:
			res[x]=m2[x]
	return res

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

counts = {}
for i in range(1,21):
	m = factorint(i)
	counts = merge_using_max(counts,m)
ans = 1
for i in counts.keys():
	ans *= (i**counts[i])
print(ans)