with open("/Users/syamk/Downloads/0022_names","r") as f:
	content = f.read()
	names = content.split(",");
	c = 'A'
	value = {}
	for i in range(26):
		value[c] = ord(c);
		c = chr(ord(c)+1)
	print(value)
	ans = 0
	for i in range(0,len(names)):
		ans += (i+1)*(sum(value[x] for x in names[i]))
	print(ans)	
