str = input()

# Write your code here!
li = list()
flag = True

for s in str:
    if s == "(":
        li.append(s)
    elif s == ")":
        if len(li) == 0:
            flag = False
            break
        li.pop(0)
    
if len(li)==0 and flag==True:
    print("Yes")
else:
    print("No")
    

    