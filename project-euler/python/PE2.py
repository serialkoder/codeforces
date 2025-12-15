a = 1
b = 2
sum = 2
fib = 0
while fib <= 4000000:
	fib = a + b
	a,b = b,fib
	if fib%2 == 0 :
		sum += fib

print(sum)
