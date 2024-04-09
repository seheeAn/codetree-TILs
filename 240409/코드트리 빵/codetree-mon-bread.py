# 1~m 사람들이 각각 1~m분에 출발 -> 목표 지점이 전부 다름
# n*n 격자

# 2. 편의점에 도착했다면 멈추고, 다른 사람들은 해당 편의점 칸을 못지나감. (다음 턴부터)
# 3. 현재 시간이 t분이면 t번 사람은 목적지 편의점과 가장 가까운 베이스캠프에 들어감 (행->열이 작으면 우선순위) 시간 소요 x
#   -> 이 시점 부터는 다른 사람들은 해당 베이스 캠프를 못지나감. (다음턴부터)
# 4. 총 몇 분 후에 모두 편의점에 도착하는 지
# 추가사항: 한 칸에 두명이상 가능. 도달 못하는 경우는 없음, 좌표는 1*1부터 시작

# 입력
N, M = map(int, input().split())
basecamp = [[0] * (N+2)] # 베이스캠프 (출발 위치)
for i in range(N):
    basecamp.append([0] + list(map(int, input().split())) + [0])
basecamp.append([0]*(N+2))

end = [[0,0] for _ in range(M+1)] # 도착지 정보 (편의점 위치)
for i in range(1,M+1):
    row, col = map(int, input().split())
    end[i] = [row,col]

people = [[0,0,-1] for _ in range(M+1)] # 사람들의 현재 좌표, -1: 출발 안함. 0: 도착 안함 1:도착함
maps = [[1 for _ in range(N+2)] for _ in range(N+2)] # 이동 가능 여부 표시
for i in range(1, N+1):
    for j in range(1,N+1):
        maps[i][j] = 0

finish = 0 #도착한 사람 수 (M이면 종료)

# 상좌우하로 한칸 이동 후 최단거리 탐색
dr = [-1, 0, 0, 1]
dc = [0, -1, 1, 0]

# 1. 모두 본인의 목적지를 향해 최단거리로 1칸 움직임. 상좌우하
# 최단거리: 상하좌우 인접한 칸 중 이동 가능한 칸으로만 이동하여 도달하기까지 거쳐야 하는 칸의 수가 최소
def people_move():
    global people, finish
    for idx in range(1,M+1):
        pr,pc, state = people[idx]
        er, ec = end[idx]
        if state != 0 : # 시작 안했거나 도착함.
            continue

        min_route = N*N+10
        for i in range(4):
            r, c = pr + dr[i], pc + dc[i]
            # print(r,c)
            if maps[r][c] != 0: # 이동 불가 지역
                continue
            if r == er and c == ec: # 한칸 이동했더니 도착지
                people[idx] = [r,c,1]
                finish += 1
                continue

            visit = [[0 for _ in range(N+1)] for _ in range(N+1)]
            queue = list()
            queue.append([r,c,0])
            visit[r][c] = 1
            visit[pr][pc] = 1

            while queue:
                curr_r, curr_c, route = queue.pop(0)
                if curr_r==er and curr_c==ec:
                    if min_route > route: # 최단거리면
                        min_route = route
                        people[idx] = [r, c, 0] # 위치 갱신
                    break

                for d in range(4):
                    nr, nc = curr_r+dr[d], curr_c + dc[d]
                    if maps[nr][nc] == 0 and visit[nr][nc] == 0:
                        queue.append([nr,nc,route+1])
                        visit[nr][nc] = 1
            # print(min_route)
# 2. 현재 시간이 t분이면 t번 사람은 목적지 편의점과 가장 가까운 베이스캠프에 들어감 (행->열이 작으면 우선순위)
def go_basecamp(t):
    global people, maps
    er, ec = end[t]

    queue = list()
    visit = [[0 for _ in range(N+1)] for _ in range(N+1)]
    queue.append([er,ec,0])
    visit[er][ec] = 1
    min_route = N*N+10
    min_r, min_c = N+1,N+1
    while queue:
        r, c, cnt = queue.pop(0)
        if cnt > min_route:
            break
        if basecamp[r][c] == 1:
            if min_route > cnt:
                min_route = cnt
                min_r, min_c = r, c
            elif min_route == cnt:
                if min_r > r:
                    min_r, min_c = r, c
                elif min_r == r and min_c > c:
                    min_c = c
            continue

        for i in range(4):
            nr = r+dr[i]
            nc = c+dc[i]
            if maps[nr][nc] == 0 and visit[nr][nc] == 0:
                queue.append([nr,nc, cnt+1])
                visit[nr][nc] = 1

    maps[min_r][min_c] = t
    people[t] = [min_r,min_c,0]

# 3. 갈 수 없는 곳 갱신 (maps)
def check_maps():
    global maps
    for idx in range(M+1):
        pr, pc, state = people[idx]
        if state == 1:
            maps[pr][pc] = idx

# 4. 모두 도착했다면 종료

time = 1
while True:
    # print(time)
    people_move()
    if time <= M:
        go_basecamp(time)
    check_maps()
    if finish == M:
        break
    # print(maps)
    # print(people)
    # print(end)
    time += 1

print(time)