from collections import defaultdict

def is_prime(n):
    count = 0
    if n <= 1:
        return False
    if n == 2 or n == 3 or n == 5:
        return True
    for i in range(2,int(n**0.5)+1):
        if n%i==0:
            return False
    return True

prime_perms = defaultdict(list)
for i in range(1000,10000):
    if is_prime(i):
        x = list(str(i))
        x.sort()
        ind = ''.join(x)
        prime_perms[ind].append(i)

def is_there_an_AP(data):
    n = len(data)
    for i in range(0,n):
        for j in range(i+1,n):
            diff = data[j]-data[i]
            target = data[j] + diff
            if target in data:
                print(f"{data[i]}{data[j]}{target}")

for k in prime_perms.keys():
    is_there_an_AP(prime_perms[k])