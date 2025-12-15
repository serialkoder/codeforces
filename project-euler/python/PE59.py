import string
from itertools import product

letters = string.ascii_lowercase  # 'abcdefghijklmnopqrstuvwxyz'

combs_with_rep = list(product(letters, repeat=3))

# Optional: Convert tuples to strings
combs_as_strings = ["".join(c) for c in combs_with_rep]


def load_words():
    with open("/usr/share/dict/words") as f:
        return {line.strip().lower(): True for line in f}


word_map = load_words()

# Optional: Print total count
print("Total combinations:", len(combs_as_strings))  # 26^3 = 17576
data = []
with open("/Users/serialcoder/Documents/ProjectEulerPython/0059_cipher.txt") as f:
    for line in f:
        data = line.strip().split(",")
max_count = 0
for c in combs_as_strings:
    cipher = [c[i % 3] for i in range(len(data))]
    message = [int(data[i]) ^ ord(cipher[i]) for i in range(len(data))]
    word = ("".join(map(chr, message))).split(" ")
    count = 0
    for w in word:
        if w in word_map:
            count += 1
    if count > max_count:
        max_count = count
        print(word, c)
        print(sum(message))
