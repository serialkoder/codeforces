import math



for i in range(10,100):
	for j in range(i+1,100):
		if i%j == 0:
			continue
		gcd_ = math.gcd(i,j)

		while i%gcd_== 0:
			i // = gcd_
		while j%gcd_== 0:
			j // = gcd_

