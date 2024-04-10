# n*n, 무기, 플레이어(능력치)
# 1. 향한 방향대로 한칸 이동. 외곽이면 정반대 방향으로 방향을 바꾸어 1칸
# 2. 해당 칸에 총이 있다면 소유하고 있는 총과 비교해서 더 쎈 총을 갖고 나머지 총을 격자에 내려놓음

# k라운드 종료 후 플레이어 포인트 출력
# *hidden: 총은 칸 하나에 복수개일 수도 잇음 (원래있던 총 + 플레이어가 져서 내려놓은 총)

n,m,k = map(int, input().split())
players = [[0]*4 for _ in range(m+1)] # r,c,d,s
players_gun = [0]*(m+1)
players_point = [0]*(m+1)
dr = [-1,0,1,0]
dc = [0,1,0,-1] #상우하좌 (오른쪽 회전)
guns = [[[] for _ in range(n+1)] for _ in range(n+1)]
players_map = [[0 for _ in range(n+1)] for _ in range(n+1)]
for i in range(1,n+1):
    tmp = [0] + list(map(int, input().split()))
    for j in range(1,n+1):
        guns[i][j].append(tmp[j])
for i in range(1, m+1):
    r,c,d,s = map(int,input().split())
    players[i] = [r,c,d,s]
    players_map[r][c] = i

# 총 획득
def select_gun(idx):
    global players_gun, guns
    r, c, d, s = players[idx]
    having_gun = players_gun[idx]
    field_gun = max(guns[r][c])
    if having_gun < field_gun:
        guns[r][c].append(having_gun)
        guns[r][c].remove(field_gun)
        players_gun[idx] = field_gun

# 플레이어 싸움
def fight(idx):
    global players, players_map, players_point, guns, players_gun
    # new player 정보
    r,c,new_d,new_s = players[idx]
    new_gun = players_gun[idx]
    # old player 정보
    old_idx = players_map[r][c]
    r, c, old_d, old_s = players[old_idx]
    old_gun = players_gun[old_idx]

    # 1. 초기능력치+총공격력 (같으면 초기 능력치 우선순위)로 승패 결정
    if new_gun+new_s > old_gun+old_s:
        winner, defeat = idx, old_idx
    elif new_gun+new_s == old_gun+old_s:
        if new_s > old_s:
            winner, defeat = idx, old_idx
        else:
            winner, defeat = old_idx, idx
    else:
        winner, defeat = old_idx, idx

    # 이기면 총합능력치의 차이만큼 포인트 획득, 해당 칸에서 총 획득
    players_point[winner] += abs((new_gun+new_s)-(old_gun+old_s))
    # 지면 총을 격자에 내려놓고 원래 가지고 있던 방향대로 한칸 이동
    # 이동 칸에 다른 플레이어가 있거나 격자 밖이면 오른쪽으로 90도씩 회전해서 빈칸에 이동 -> 총획득
    guns[r][c].append(players_gun[defeat])
    players_gun[defeat] = 0
    r,c,dd,ds = players[defeat]
    for i in range(4):
        nd = (dd+i) % 4
        nr,nc = r+dr[nd], c+dc[nd]
        if 0<nr<n+1 and 0<nc<n+1:
            if players_map[nr][nc] == 0:
                players_map[nr][nc] = defeat
                players_map[r][c] = winner
                players[defeat] = [nr,nc,nd,ds]
                select_gun(defeat)
                break
    # 승자 총 획득
    select_gun(winner)

# 플레이어 이동
def player_move():
    global players_map, players
    for idx in range(1,m+1):
        r,c,d,s = players[idx] #상우하좌
        if r == 1 and d == 0: #방향전환
            d = 2
        elif c == n and d == 1:
            d = 3
        elif r == n and d == 2:
            d = 0
        elif c == 1 and d == 3:
            d = 1
        nr,nc = r+dr[d], c+dc[d]
        players[idx] = [nr, nc, d, s] #player 정보 갱신
        players_map[r][c] = 0

        if players_map[nr][nc] == 0: # 사람없음
            players_map[nr][nc] = idx
            select_gun(idx)
        else: # 사람있음.
            fight(idx)

for round in range(k):
    player_move()

answer = ''
for i in range(1,m+1):
    answer += str(players_point[i]) + ' '
print(answer)