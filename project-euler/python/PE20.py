

LIM = 100
ans = 1
while LIM>0 :
	ans = ans*LIM
	while ans%10==0:
		ans//=10
	LIM-=1
print(sum(int(x) for x in str(ans)))