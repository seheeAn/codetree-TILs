N = int(input())
seat = input()

# Write your code here!
seat_list = []
for i in seat:
    seat_list.append(i)

ans = -1
for i in range(len(seat_list)):
    if seat_list[i] == '0':
        seat_list[i] = '1'

        seat_idx = list()
        for idx, p in enumerate(seat_list):
            if p == '1':
                seat_idx.append(idx)
        
        min_dis = len(seat)
        for j in range(1, len(seat_idx)):
            dis = seat_idx[j] - seat_idx[j-1]
            if min_dis >= dis:
                min_dis = dis

        if ans <= min_dis:
            ans = min_dis
            seat_list

        seat_list[i] = '0'

print(ans)

