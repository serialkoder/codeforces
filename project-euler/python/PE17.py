from num2words import num2words

def count(string):
    count = 0
    for x in string:
        if x != ' ' and x != '-':
            count += 1
    return count

def format_number(n):
    # Adjust spacing to match your style
    words = num2words(n).replace(" and ", "  and  ")
    return words

ans = 0
for i in range(1, 1001):
    result = format_number(i)
    char_count = count(result)
    ans += char_count

print(ans)