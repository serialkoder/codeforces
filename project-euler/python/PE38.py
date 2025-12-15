def has_duplicate_digits(n):
	x = list(n)
	return len(set(x))<len(x)

def has_all_digits_1_to_9_once(s):
    return set(s) == set('123456789') and len(s) == 9
	

for i in range(1,10000):
	num = ""
	for j in range(1,10):
		num = num + str(i*j)
		if has_duplicate_digits(num):
			break
		if has_all_digits_1_to_9_once(num):
			print(num)






