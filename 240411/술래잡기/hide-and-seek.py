# n*n 술래는 1명, 정중앙 시작
# m명의 도망자, 좌우(오른쪽 시작)/상하(아래쪽 시작)로만 움직임
# h개의 나무, 나무와 도망자가 초기에 겹쳐서 시작 가능
# 도망자 -> 술래 순으로 움직임 k번 반복

n,m,h,k = map(int, input().split())
maps = [[-1 for _ in range(n+2)] for _ in range(n+2)]
trees = [[0 for _ in range(n+2)] for _ in range(n+2)]
peoples = list()
for i in range(1,n+1):
    for j in range(1,n+1):
        maps[i][j] = 0
for i in range(m):
    r,c,d = map(int, input().split()) #1=우 2=하
    peoples.append([r,c,d])
    maps[r][c] = 1
for i in range(h):
    r,c = map(int, input().split())
    trees[r][c] = 1
dr = [-1,0,1,0] #상우하좌
dc = [0,1,0,-1]
mid = n//2+1
chaser = [mid,mid,0]
c_route = list()
c_idx = 0
reverse = 1 #안에서 밖 = 1 밖에서 안 = -1
answer = 0
caught = list()
# 0. 술래의 경로가 reverse 되거나 처음 시작할 때 호출
def init_route():
    global c_route
    c_route = []
    for i in range(1, n):
        if i == n-1:
            c_route.append(i)
        c_route.append(i)
        c_route.append(i)

# 1. 도망자 이동
# 술래와의 거리가 3이하인 도망자만 움직임
# 거리 = abs(x1-x2) + abs(y1-y2)
# 격자를 벗어나지 않으면, 움직이려는 칸에 술래가 없을 때 한칸 이동(나무 o)
# 격자를 벗어나면 방향을 반대로 틀고, 해당 칸에 술래가 없으면 한칸 이동
# 도망자끼리 겹칠 수 있음
def runner_move():
    global peoples, maps
    for idx in range(m):
        if idx in caught:
            continue
        pr,pc,pd = peoples[idx]
        cr,cc,cd = chaser
        if (abs(pr-cr) + abs(pc-cc)) <= 3: #도망
            nr,nc = pr+dr[pd], pc+dc[pd]

            if maps[nr][nc] < 0: # 격자 밖이면 방향, 좌표 보정
                if pd == 0 and nr == 0: #상
                    pd = 3
                elif pd == 1 and nc == n+1: #우
                    pd = 3
                elif pd == 2 and nr == n+1 : #하
                    pd = 0
                elif pd == 3 and nc == 0: #좌
                    pd = 1
                nr,nc = pr+dr[pd], pc+dc[pd]
            if nr==cr and nc==cc:
                continue

            maps[pr][pc] -= 1
            maps[nr][nc] += 1
            peoples[idx] = [nr,nc,pd]

# 2. 술래 이동
# 위방향으로 시작해서 달팽이 모양으로 움직임.
# (1,1)혹은 중심에 도달하면 다시 거꾸로
# 이동 후 위치가 이동방향이 틀어지는 지점이라면 방향을 바로 틈
def chaser_move():
    global chaser, c_route, c_idx, reverse
    cr,cc,cd = chaser
    ncr, ncc = cr+dr[cd], cc+dc[cd]
    c_route[c_idx] -= 1
    if c_route[c_idx] == 0: #방향 전환
        if [ncr,ncc] == [mid,mid] or [ncr,ncc] == [1,1]: # 경로 뒤집기
            reverse *= -1
            if cd == 0:
                cd = 2
            elif cd == 2:
                cd = 0
            init_route()
        elif reverse == -1:
            if cd == 0:
                cd = 3
            else:
                cd -= 1
            c_idx -= 1
        elif reverse == 1:
            cd = (cd+1) % 4
            c_idx += 1
    chaser = [ncr,ncc,cd]

# 3. 도망자 잡기
# 이동 직후 턴을 넘기기 전 시야 내에 있는 도망자를 잡음 (시야는 술래 포함 3칸)
# 나무가 있다면 해당 칸은 안보임
# 현재턴 * 잡힌 도망자 수 만큼 점수 얻음. 잡힌 도망자는 사라짐
def catch_runner(t):
    global maps, answer,caught,peoples
    cr,cc,cd = chaser
    for i in range(3):
        nr,nc = cr+i*dr[cd], cc+i*dc[cd]
        if not(0<nr<n+1 and 0<nc<n+1):
            break
        if maps[nr][nc] >= 0:
            if trees[nr][nc] == 1:
                continue
            answer += t*maps[nr][nc]
            maps[nr][nc] = 0
            for idx in range(m):
                pr, pc, pd =peoples[idx]
                if pr==nr and pc == nc:
                    caught.append(idx)

init_route()
for t in range(1,k+1):
    runner_move()
    chaser_move()
    catch_runner(t)

print(answer)