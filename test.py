total = 0
for i in range(10):
    print(i)
    if i == 7 and total < 100:
        i -= 1
    total += i


a = [1, 1, 2, 3, 3, 3, 4, 5, 5, 5, 3, 2, 2, 1, 0]

index = 0
while index < len(a):
    if a[index] == a[(index + 1) % len(a)]:
        a = a[:index] + a[index+1:]
        index -= 1
    index += 1
    print(a)