from collections import deque

# L x L (1,1)시작
# 빈칸, 함정, 벽
# (r,c) 좌측 상단 -> h*w 크기, 체력 k

# 1. 기사 이동
# 상하좌우 한칸 이동. 다른 기사 있으면 한칸 밀기.(연쇄)
# 벽이 있다면 이동 x
# 체스판에 사라진 기사면 이동 x

# 2. 대결
# 밀려난 기사는 피해입음. (이동한 곳에서 w x h 내의 함정 수만큼)
# 체력이 0 이하 -> 체스판에서 벗어남

# Q번 후 1.생존한 기사들이 2.받은 대미지 합

L,N,Q = map(int,input().split())
board = [[2] * (L+2)]
for _ in range(L):
    board.append([2] + list(map(int,input().split())) + [2])
board.append([2]*(L+2))
knights = [[0,0,0,0,0]]*(N+1) # sr,sc,er,ec,k
max_k = [0] * (N+1)
for i in range(1,N+1):
    r,c,h,w,k = map(int,input().split())
    knights[i] = [r,c,r+h-1,c+w-1,k]
    max_k[i] = k
q_list = [0,0] * (Q+1) #i,d
for q in range(1,Q+1):
    q_list[q] = list(map(int,input().split()))
dr = [-1,0,1,0] # 상우하좌
dc = [0,1,0,-1]
move_idx = []
can_move = True

# 1. 기사 이동
# # 상하좌우 한칸 이동. 다른 기사 있으면 한칸 밀기.(연쇄)
# # 벽이 있다면 이동 x
# # 체스판에 사라진 기사면 이동 x
def move(idx, d):
    global move_idx, can_move, knights
    sr,sc,er,ec,k = knights[idx]

    if k<=0: #죽었음
        can_move=False
        return

    nsr, nsc = sr+dr[d], sc+dc[d]
    ner, nec = er+dr[d], ec+dc[d]
    queue = deque()
    queue.append([nsr,nsc,ner,nec])

    move_idx.append(idx)
    visit = [0] * (N+1)
    visit[idx] = 1
    while queue:
        r,c,rr,cc = queue.popleft()

        for i in range(r,rr+1): #벽이있으면
            for j in range(c,cc+1):
                if board[i][j] == 2:
                    can_move = False
                    break

        for n in range(1,N+1):
            if visit[n] == 1:
                continue
            xr,xc,xrr,xcc,xk = knights[n]
            if xk <= 0:
                continue
            if (xr<=r<=xrr or xr<=rr<=xrr) and (xc<=c<=xcc or xc<=cc<=xcc):
                queue.append([xr+dr[d],xc+dc[d],xrr+dr[d],xcc+dc[d]])
                visit[n] = 1
                move_idx.append(n)

    if can_move:
        for m in move_idx:
            r,c,rr,cc,k = knights[m]
            knights[m] = [r+dr[d], c+dc[d], rr+dr[d], cc+dc[d], k]

# 2. 대결
# 밀려난 기사는 피해입음. (이동한 곳에서 w x h 내의 함정 수만큼)
# 체력이 0 이하 -> 체스판에서 벗어남
def fight():
    for ii in range(1,len(move_idx)):
        idx = move_idx[ii]
        r,c,rr,cc,k = knights[idx]
        cnt = 0
        for i in range(r,rr+1):
            for j in range(c,cc+1):
                if board[i][j] == 1:
                    cnt += 1

        knights[idx] = [r,c,rr,cc,k-cnt]


for i in range(1,Q+1):
    #초기화
    move_idx = []
    can_move = True
    idx, d = q_list[i]

    move(idx,d)
    if can_move:
        fight()
    # print(idx, d)
    # print(knights)

answer = 0
for i in range(1,N+1):
    if knights[i][-1] > 0:
        answer += (max_k[i]-knights[i][-1])

print(answer)