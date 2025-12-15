from collections import defaultdict

cubes = defaultdict(list)

for i in range(1, 50000):
    k = i**3
    x = list(str(k))
    x.sort()
    key = "".join(x)
    cubes[key].append(i**3)
    if len(cubes[key]) == 5:
        print(cubes[key][0])
        break
