current_index = 1
previous_index = 1
remaining = [10, 100, 1000, 10000, 100000, 1000000, 0]
rem_index = 0
ans = 1
for i in range(2, 1000000):
    current_index += len(str(i))
    if remaining[rem_index] > previous_index and remaining[rem_index] <= current_index:
        target_index = remaining[rem_index] - previous_index - 1
        ans *= int(str(i)[target_index])
        print(i - 1, i, previous_index, current_index, target_index)
        rem_index += 1
    previous_index = current_index
print(ans)
