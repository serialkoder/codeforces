# dx represents change in x-coordinate (horizontal movement)
dx = [-1, 0, 1, -1, 1, -1, 0, 1]

# dy represents change in y-coordinate (vertical movement)
dy = [-1, -1, -1, 0, 0, 1, 1, 1]

# Method 1: Basic file reading
def read_2d_array(filename):
    array_2d = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                # Split line by spaces and convert strings to integers
                row = [int(num) for num in line.split()]
                array_2d.append(row)
        return array_2d
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return None
    except ValueError:
        print("Error: File contains non-numeric values")
        return None

# Example usage
filename = "PE11_inp"
grid = read_2d_array(filename)

ans = 0
for i in range(0,20):
	for j in range(0,20):
		for k in range(0,8):
			prod = 1
			for l in range(1,5):
				x = i + dx[k]*l
				y = j + dy[k]*l
				if x >=0 and x < 20 and y>=0 and y < 20:
					prod *= grid[x][y]		
			ans = max(ans,prod)				

print(ans)
