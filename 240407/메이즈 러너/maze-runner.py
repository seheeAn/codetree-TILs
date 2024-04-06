# NxN (1,1)부터 시작,
# 0 빈칸 or 1~9 벽 or 출구

# K초 전에 모든 참가자가 탈출 or K초 끝
# 모든 참가자들의 이동 거리 합과 출구 좌표를 출력

# 입력
N,M,K = map(int, input().split())
maps = [[-1 for _ in range(N+2)] for _ in range(N+2)]
people = []
moves = [0] * M
for i in range(1, N+1):
    tmp = list(map(int,input().split()))
    for j in range(1, N+1):
        maps[i][j] = tmp[j-1]
for _ in range(M):
    people.append(list(map(int, input().split())))
out_r, out_c = map(int, input().split())

dr = [-1,1,0,0] # 상하좌우
dc = [0,0,-1,1]

# 게임 시작
finish = []
for k in range(K): # K초
    # 1. 참가자 이동 (동시에, 1초마다)
    # 출구까지 거리가 지금보다 가까워지는 방향으로, 움직일 수 있을 때만 이동
    # 거리는 abs(x1-x2) + abs(y1-y2)
    # 한칸에 2명이상 ok
    for idx in range(len(people)):
        if idx in finish: # 탈출한 참가자면 skip
            continue
        r,c = people[idx]
        curr_d = abs(r-out_r) + abs(c-out_c)
        for i in range(4):
            nr = r + dr[i]
            nc = c + dc[i]
            if maps[nr][nc] == 0: # 이동 가능 여부 체크
                next_d = abs(nr-out_r) + abs(nc-out_c)
                if curr_d > next_d:
                    people[idx] = [nr, nc] # 이동
                    moves[idx] += 1
                    if nr == out_r and nc == out_c: # 탈출
                        finish.append(idx)
                    break
    if len(finish) == M:  # 모두 탈출
        break

    # 2. 미로 회전
    # 한 명 이상의 참가자와 출구를 포함한 가장 작은 정사각형 선택
    # 좌상단 r -> c가 작은게 우선순위
    # 선택된 정사각형은 시계 방향 90도 회전, 내구도 -1
    min_length = N
    min_r, min_c = N,N
    for idx in range(len(people)):
        if idx in finish:
            continue
        r,c = people[idx]
        length = max(abs(out_r-r), abs(out_c-c))
        if min_length > length:
            min_length = length
            min_r, min_c = r,c
        elif min_length == length:
            if min_r > r:
                min_r, min_c = r, c
            elif min_r == r and min_c < c:
                min_c = c

    # 정사각형 좌상단 구하기
    top_left_r, top_left_c = min(min_r, out_r), min(min_c, out_c)
    bottom_right_r, bottom_right_c = max(min_r, out_r), max(min_c, out_c)
    remain_r = min_length - (bottom_right_r - top_left_r)
    remain_c = min_length - (bottom_right_c - top_left_c)
    top_left_r = max(1, top_left_r-remain_r)
    top_left_c = max(1, top_left_c-remain_c)

    # 회전
    square = [[0 for _ in range(min_length+1)] for _ in range(min_length+1)]
    for i in range(min_length+1):
        for j in range(min_length+1):
            square[i][j] = maps[top_left_r+i][top_left_c+j]
    new_map = [list(matrix[::-1]) for matrix in zip(*square)]

    # 이식
    for i in range(min_length+1):
        for j in range(min_length+1):
            if new_map[i][j] > 0:
                new_map[i][j] -= 1
            maps[i+top_left_r][j+top_left_c] = new_map[i][j]

    #출구, 사람 회전
    for idx in range(len(people)):
        r, c = people[idx]
        if top_left_r<=r<=top_left_r+min_length and top_left_c <= c <= top_left_c+min_length:
            o_r, o_c = r-top_left_r, c-top_left_c
            _r, _c = o_c, min_length+1 - o_r - 1
            r, c = _r + top_left_r, _c + top_left_c
            people[idx] = [r,c]

    o_r, o_c = out_r-top_left_r, out_c - top_left_c
    _r, _c = o_c, min_length+1 - o_r -1
    out_r, out_c = _r+top_left_r, _c+top_left_c

print(sum(moves))
print(out_r, out_c)