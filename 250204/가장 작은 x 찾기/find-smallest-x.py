n = int(input())
ranges = [tuple(map(int, input().split())) for _ in range(n)]
a, b = zip(*ranges)
a, b = list(a), list(b)

# Write your code here!
for i in range(1, 10):
    flag = False
    num = i

    for j in range(n):
        num *= 2
        if num >= a[j] and num <= b[j]:
            flag = True
        else:
            flag = False
            break
    
    if flag == True:
        print(i)
        break