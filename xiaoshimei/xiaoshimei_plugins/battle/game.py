import math

summ = 0
for i in range(8):
    summ += math.log(i+2) / 2**(i+1)

print(summ)
print(math.log(3))