from collections import defaultdict
def factors(x):
	f = set()
	temp = x
	for i in range(2,int(x**0.5)+1):		
		if temp%i == 0:
			f.add(i)
			while temp%i == 0:
				temp //= i
	if temp > 1:
		f.add(temp)
	return f

result = defaultdict(set)
start = 5
for i in range(1,10):
	result[i]=factors(i)
print(result)	

while True:
	found = True
	for i in range(start,start-4,-1):
		if len(result[i])==4:
			continue
		else:
			found = False
			break
	if found:
		print(start-3)
		break
	start += 1
	result[start] = factors(start)
	if len(result)>5:
		del result[start-4]
