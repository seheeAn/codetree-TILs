# NxN (1,1)부터 시작,
# 0 빈칸 or 1~9 벽 or 출구

# K초 전에 모든 참가자가 탈출 or K초 끝
# 모든 참가자들의 이동 거리 합과 출구 좌표를 출력

# 입력
N,M,K = map(int, input().split())

maps = [[-1 for _ in range(N+2)] for _ in range(N+2)]
for i in range(1, N+1):
    tmp = list(map(int,input().split()))
    for j in range(1, N+1):
        maps[i][j] = tmp[j-1]

people = []
for _ in range(M):
    people.append(list(map(int, input().split())))

out = list(map(int, input().split()))
moves = 0

sr, sc, square_size = 0,0,0

# 1. 참가자 이동 (동시에, 1초마다)
# 출구까지 거리가 지금보다 가까워지는 방향으로, 움직일 수 있을 때만 이동
# 거리는 abs(x1-x2) + abs(y1-y2)
# 한칸에 2명이상 ok
def move_people():
    global out, moves
    for p in range(M):
        if people[p] == out:
            continue
        pr, pc = people[p]
        outr, outc = out

        if pr != outr:
            npr, npc = pr, pc
            if pr < outr:
                npr += 1
            else:
                npr -= 1

            if maps[npr][npc] == 0:
                people[p] = [npr, npc]
                moves += 1
                continue

        if pc != outc:
            npr, npc = pr, pc
            if pc < outc:
                npc += 1
            else:
                npc -=1

            if maps[npr][npc] == 0:
                people[p] = [npr, npc]
                moves += 1
                continue


# 2. 미로 회전
# 한 명 이상의 참가자와 출구를 포함한 가장 작은 정사각형 선택
# 좌상단 r -> c가 작은게 우선순위
def find_square():
    global out, sr, sc, square_size
    outr, outc = out
    #왼쪽 좌상단 부터 사각형 하나씩 만들기

    for size in range(2, N):
        for i in range(1, N+1 - size+1):
            for j in range(1, N+1 - size+1):
                r1, r2, c1, c2 = i, i+size-1, j, j+size-1
                if not(r1<=outr<=r2 and c1<=outc<=c2):
                    continue

                is_people_in_square = False
                for p in people:
                    pr, pc = p
                    if (r1<=pr<=r2 and c1<=pc<=c2) and not(pr==outr and pc == outc):
                        is_people_in_square = True
                        break

                if is_people_in_square == True:
                    sr, sc = r1, c1
                    square_size = size
                    return

# 회전
# 선택된 정사각형은 시계 방향 90도 회전, 내구도 -1
def rotate_square():
    global square_size, sr, sc, out, people

    square = [[0 for _ in range(square_size)] for _ in range(square_size)]
    for i in range(square_size):
        for j in range(square_size):
            square[i][j] = maps[sr+i][sc+j]
    new_map = [list(matrix[::-1]) for matrix in zip(*square)]

    # 이식
    for i in range(square_size):
        for j in range(square_size):
            if new_map[i][j] > 0:
                new_map[i][j] -= 1
            maps[i+sr][j+sc] = new_map[i][j]

    #출구, 사람 회전
    for idx in range(M):
        r, c = people[idx]
        if sr<=r<sr+square_size and sc <= c < sc+square_size:
            o_r, o_c = r-sr, c-sc
            _r, _c = o_c, square_size - o_r - 1
            r, c = _r + sr, _c + sc
            people[idx] = [r,c]

    outr, outc = out
    o_r, o_c = outr-sr, outc-sc
    _r, _c = o_c, square_size - o_r -1
    out = [_r+sr, _c+sc]


# 게임 시작
for k in range(K): # K초
    move_people()

    is_all_escape = True
    for i in range(M):
        if people[i] != out:
            is_all_escape = False

    if is_all_escape == True:
        break

    find_square()
    rotate_square()

print(moves)
print(out[0], out[1])