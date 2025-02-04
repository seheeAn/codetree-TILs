n = int(input())
ranges = [tuple(map(int, input().split())) for _ in range(n)]
a, b = zip(*ranges)
a, b = list(a), list(b)

# Write your code here!
for i in range(1, 11):
    flag = False
    num = i

    for j in range(n):
        if num * 2**(j+1) >= a[j] and num *2**(j+1) <= b[j]:
            flag = True
    for j in range(n):
        if num * 2**(j+1) >= a[j] and num *2**(j+1) <= b[j]:
            flag = True
        else:
            flag = False
            break
    
    if flag == True:
        print(i)
        break

테스트케이스


결과


코드 실행


제출 및 채점



        else:
            flag = False
            break
    
    if flag == True:
        print(i)
        break