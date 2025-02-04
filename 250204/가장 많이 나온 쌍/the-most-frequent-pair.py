n, m = map(int, input().split())
pairs = [tuple(map(int, input().split())) for _ in range(m)]

# Write your code here!
pair_dict = {}

for p in pairs:
    a, b = p
    small, big = min(a, b), max(a,b)
    if (small, big) not in pair_dict:
        pair_dict[(small,big)] = 1
    else:
        pair_dict[(small,big)] += 1

max_num = -1
for p in pair_dict.keys():
    if max_num <= pair_dict[p]:
        max_num = pair_dict[p]

print(max_num)