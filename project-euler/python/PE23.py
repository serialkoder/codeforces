from math import sqrt
LIM = 28123
count = 0
def sum_of_divisors(n):
	sum_ = 1
	num = n
	for i in range(2,int(sqrt(n))+1):
		factor_count = 0
		if num%i==0:
			while num%i==0:
				factor_count+=1;
				num//=i
		sum_ *= (i**(factor_count+1)-1)//(i-1)
	if num > 1:
		sum_ *= (num**2-1)//(num-1)
	return sum_-n
abundant_numbers = [i for i in range(1,LIM) if sum_of_divisors(i)>i]
seen = set()
for i,first in enumerate(abundant_numbers):
	for second in abundant_numbers[i:]:
		seen.add(first+second)
		
ans = sum(i for i in range(1,28125) if i not in seen)

print(ans)