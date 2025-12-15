import string

with open("/Users/serialcoder/Downloads/0022_names.txt","r") as f:
	content = f.read()
	content = content.replace('"',"")
	names = sorted(content.split(","));
	c = 'A'
	value = {c:ord(c)-64 for c in string.ascii_uppercase}
	ans = sum(i*sum(value[x] for x in name) for i,name in enumerate(names,start=1))
	print(ans)	
