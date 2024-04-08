# N*M 격자
# 0이하인 포탑은 공격 불가
# K턴, 부서지지 않은 포탑이 1개이면 중지

# 5. 출력
# 전체 과정 종료 후 가장 강한 포탑의 공격력 출력

#입력
N,M,K = map(int, input().split())
maps = []
handicap = N+M
for n in range(N):
    maps.append(list(map(int, input().split())))
last_attack = [[-1 for _ in range(M)] for _ in range(N)]

broke_num = 0
for n in range(N):
    for m in range(M):
        if maps[n][m] == 0:
            broke_num += 1

inside_attack = [] #공격 관련자 저장

#1.공격자 선정
# 가장 약한 포탑이 공격자로 선정 -> N+M만큼 공격력 증가
# 공격력이 가장 낮음 -> 최근에 공격한 포탑 ->
# 행과 열의 합이 가장 큰 포탑 -> 열 값이 가장 큰 포탑
attacker = [10, 10, 10000]
reciever = [-1,-1, 0]
def find_attacker():
    global attacker, inside_attack
    row, col, point = attacker
    for i in range(N):
        for j in range(M):
            if 0 < maps[i][j] < point:
                point = maps[i][j]
                row, col = i, j
            elif maps[i][j] == point:
                if last_attack[row][col] < last_attack[i][j]:
                    row, col = i,j
                elif last_attack[row][col] == last_attack[i][j]:
                    if row+col < i+j:
                        row, col = i, j
                    elif row+col == i+j and col<j:
                        row, col = i, j
    attacker = [row, col, point+handicap]
    inside_attack.append([row,col])

#2. 공격자 선정
# 가장 강한 포탑을 공격
# 공격력이 가장 높음 -> 공격한지 가장 오래됨 -> 행과 열의 합이 가장 작음 -> 열 값이 가장 작음
def find_reciever():
    global reciever, inside_attack
    at_row, at_col, at_point = attacker
    row, col, point = reciever
    for i in range(N):
        for j in range(M):
            if i == at_row and j == at_col:
                continue
            if point < maps[i][j]:
                point = maps[i][j]
                row, col = i, j
            elif point == maps[i][j]:
                if last_attack[row][col] > last_attack[i][j]:
                    row, col = i, j
                elif last_attack[row][col] == last_attack[i][j]:
                    if row+col > i+j:
                        row, col = i,j
                    elif row+col == i+j and col > j:
                        row, col = i, j
    reciever = [row,col,point]
    inside_attack.append([row,col])

# 3-1. 레이저 공격
# 상하좌우 4방향 이동, 부서진 포탑이 있으면 못지나감, 막힌 방향으로 진행시 반대편으로 나옴
# 최단 경로로 공격 -> 우하좌상 우선순위 가짐 -> 경로가 없으면 포탄 공격
# 공격자의 공격력 만큼 피해입음. 공격력 -= 피해량
# 경로에 공격대상 이외의 포탑들은 공격력//2만큼 피해받음
def laiser_attack():
    global maps, broke_num
    dr = [0,1,0,-1] #우하좌상
    dc = [1,0,-1,0]
    at_r, at_c, at_power = attacker
    re_r, re_c, re_power = reciever

    is_reach = False
    visit = [[0 for _ in range(M)] for _ in range(N)]
    route = [[[-1, -1] for _ in range(M)] for _ in range(N)]
    que = [[at_r, at_c]]
    visit[at_r][at_c] = 1

    while que:
        r, c = que.pop(0)
        if r == re_r and c == re_c: #도착
            is_reach = True
            break

        for i in range(4):
            nr, nc = r+dr[i], c+dc[i]
            if nr == N:
                nr = 0
            elif nr == -1:
                nr = N-1
            if nc == M:
                nc = 0
            elif nc == -1:
                nc = M-1

            if visit[nr][nc] == 0 and maps[nr][nc] > 0:
                route[nr][nc] = [r, c]
                visit[nr][nc] = 1
                que.append([nr,nc])

    if is_reach:
        _r, _c = re_r, re_c
        while True:
            if _r == at_r and _c == at_c:
                break

            if _r == re_r and _c == re_c:
                maps[_r][_c] -= at_power
            else:
                inside_attack.append([_r,_c])
                maps[_r][_c] -= at_power//2
            _r, _c = route[_r][_c]
            if maps[_r][_c] <= 0:
                broke_num += 1
    return is_reach

# 3-2. 포탄 공격
# 공격 대상에 포탄 던짐. 주위 8방향은 //2만큼 피해 (공격자 제외)
# 가장자리면 반대편 격자에 피해.
def bomb_attack():
    global inside_attack, maps, broke_num
    at_r, at_c, at_power = attacker
    re_r, re_c, re_power = reciever

    maps[re_r][re_c] -= at_power
    if maps[re_r][re_c] <= 0:
        broke_num+=1

    dr = [0,0,-1,1,-1,1,-1,1]
    dc = [-1,1,0,0,-1,-1,1,1]
    for i in range(8):
        nr, nc = re_r + dr[i], re_c + dc[i]
        if nr == N:
            nr = 0
        elif nr == -1:
            nr = N - 1
        if nc == M:
            nc = 0
        elif nc == -1:
            nc = M - 1

        if maps[nr][nc] <= 0:
            continue
        if nr == at_r and nc == at_c:
            continue

        maps[nr][nc] -= at_power//2
        inside_attack.append([nr,nc])
        if maps[nr][nc] <= 0:
            broke_num += 1

# 4. 포탑 정비
# 부서지지 않은 포탑 중 공격과 무관한 포탑은 +1
def finish_turn():
    global maps
    for i in range(N):
        for j in range(M):
            if [i,j] not in inside_attack and maps[i][j] > 0:
                maps[i][j] += 1

for k in range(K):
    inside_attack = [] #초기화 ... 아 제발 좀...;;;;
    attacker = [10, 10, 10000]
    reciever = [-1, -1, 0]

    if broke_num == N*M-1: # 하나 남으면 게임 종료
        break

    find_attacker()
    row,col,point = attacker
    maps[row][col] = point
    last_attack[row][col] = k

    find_reciever()
    is_reach = laiser_attack()
    if not is_reach:
        bomb_attack()

    finish_turn()


answer = 0
for i in range(N):
    for j in range(M):
        if maps[i][j] > answer:
            answer = maps[i][j]

print(answer)