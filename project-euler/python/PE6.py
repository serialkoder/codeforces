from itertools import accumulate
LIM = 100
sum_of_squares = sum(x**2 for x in range(1,LIM+1))
square_of_sum = (sum(x for x in range(1,LIM+1)))**2
print(square_of_sum-sum_of_squares)