def is_prime(n):
    if n < 2: return False
    if n in (2, 3): return True
    if n % 2 == 0 or n % 3 == 0: return False
    for i in range(5, int(n**0.5)+1, 6):
        if n % i == 0 or n % (i+2) == 0:
            return False
    return True

prime_prefix_sum= list()

i = 1
total_sum = 0
while  total_sum <= 1000000 :
    i += 1
    if is_prime(i):
        if total_sum+i <= 1000000:
            total_sum += i
            prime_prefix_sum.append(total_sum)
        else:
            break
prime_prefix_sum.sort(reverse=True)            
max_ = 0
ans = 0
for i in range(0,len(prime_prefix_sum)):
    for j in range(i+max_+1,len(prime_prefix_sum)):
        if is_prime(prime_prefix_sum[i]-prime_prefix_sum[j]):
            cur = abs(i-j)
            if cur > max_:
                max_ = cur
                ans = prime_prefix_sum[i]-prime_prefix_sum[j]

print(ans)






    


