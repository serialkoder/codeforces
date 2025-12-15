with open("PE13_inp", 'r') as file:
	total_sum =  sum(int(line.strip()) for line in file)
print(str(total_sum)[0:10])
