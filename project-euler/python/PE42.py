triangle_numbes = set([i * (i + 1) // 2 for i in range(1, 100)])
with open("0042_words.txt") as f:
    words = f.readline().strip().replace('"', "").split(",")

char_index = {}
for ind, char in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 1):
    char_index[char] = ind
ans = 0
for i in words:
    if sum(char_index[x] for x in i) in triangle_numbes:
        ans += 1
print(ans)
