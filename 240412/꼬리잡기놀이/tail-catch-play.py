# n*n 각 격자마다 한팀씩 줄줄이 이동
# 공은 우상좌하 (그림참고) 방향으로 던져짐
# 최초로 공과 만나는 사람이 점수를 얻음. (점수 = 머리부터 k번째 -> k**2)
# 공 획득 팀은 머리사람과 꼬리사람이 바뀜

# 1.이동
# 2.공던짐
# 3.점수획득 + 방향 바뀜
# 4.각 팀이 얻게되는 점수의 총합 출력

n,m,k = map(int, input().split())
maps = []
team_info = []
for i in range(n):
    maps.append(list(map(int,input().split())))
for i in range(n):
    for j in range(n):
        if maps[i][j] == 1:
            team_info.append([i,j])
dr = [0,-1,0,1]
dc = [1,0,-1,0]
answer = 0

# 1.이동
def move():
    global maps, team_info
    for idx in range(m):
        hr,hc = team_info[idx]
        queue = []
        visit = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(4):
            nhr,nhc = hr+dr[i], hc+dc[i]
            if not(0<=nhr<n and 0<=nhc<n):
                continue
            if maps[nhr][nhc] == 4: #머리 변경
                maps[nhr][nhc] = 1
                team_info[idx] = [nhr,nhc]
            elif maps[nhr][nhc] == 2 or maps[nhr][nhc]==3: # 꼬리 찾기
                queue.append([nhr, nhc])
                maps[hr][hc] = maps[nhr][nhc]
                visit[nhr][nhc] = 1
                visit[hr][hc] = 1

        while queue:
            r, c = queue.pop(0)
            if maps[r][c] == 3:
                maps[r][c] = 4
                break

            for i in range(4):
                nr, nc = r+dr[i], c+dc[i]
                if not(0<=nr<n and 0<=nc<n):
                    continue
                if visit[nr][nc] != 0:
                    continue
                if maps[nr][nc] == 2 or maps[nr][nc] == 3:
                    visit[nr][nc] = 1
                    maps[r][c] = maps[nr][nc]
                    queue.append([nr,nc])

# 2.공던짐
def ball(turn): #0~k-1
    turn = turn%(4*n)
    if 0<=turn<n:
        for i in range(n):
            if maps[turn][i] in [1,2,3]:
                return turn,i
    elif n<=turn<2*n:
        turn -= n
        for i in range(n-1,-1,-1):
            if maps[i][turn] in [1,2,3]:
                return i,turn
    elif 2*n<=turn<3*n:
        turn -= 2*n
        for i in range(n-1, 1, -1):
            if maps[n-turn-1][i] in [1,2,3]:
                return n-turn-1, i
    elif 3*n <= turn <4*n:
        turn -= 3*n
        for i in range(n):
            if maps[i][n-turn-1] in [1,2,3]:
                return i, n-turn-1
    return -1,-1

# 3. 점수얻고 방향 전환
def score(row,col):
    global answer, maps, team_info
    queue =list()
    visit = [[0 for _ in range(n)] for _ in range(n)]
    queue.append([row,col,1])
    visit[row][col] = 1
    hr,hc = -1,-1
    tr,tc = -1,-1
    while queue:
        r,c,k = queue.pop(0)
        if maps[r][c] == 1:
            answer += k**2
            maps[r][c] = 3
            hr,hc = r,c

        elif maps[r][c] == 3:
            maps[r][c] = 1
            tr,tc = r,c

        for i in range(4):
            nr, nc = r+dr[i], c+dc[i]
            if not(0<=nr<n and 0<=nc<n):
                continue

            if visit[nr][nc] == 1:
                continue

            if maps[nr][nc] in [1,2,3]:
                queue.append([nr,nc,k+1])
                visit[nr][nc] = 1

    # 바꾸기
    for idx in range(m):
        if team_info[idx] == [hr,hc]:
            team_info[idx] = [tr,tc]

for round in range(k):
    move()
    row,col = ball(round)
    if [row,col] != [-1,-1]:
        score(row,col)

print(answer)