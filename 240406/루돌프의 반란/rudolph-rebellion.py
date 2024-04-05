# 산타 1~P
# 루돌프가 산타 박치기;; 루돌프 잡아야함
# NxN 격자 (r,c) 좌상단 (1,1) #주의...
# M개의 턴 매 턴마다 루돌프 -> 산타 번호 순으로 한번씩 움직임
# 기절하거나 격자 밖으로 빠져나가 탈락한 산타는 제외됨
# 거리는 (r1-r2)^2 + (c1-c2)^2

# M번의 턴이 모두 종료 or P명의 산타가 모두 탈락,
# 매 턴 이후 탈락 안한 산타들에게는 1점 부여
# 게임 종료 후 각 산타가 얻은 최종 점수

# 입력
N, M, P, C, D = map(int, input().split())
r_r, r_c = map(int, input().split())
maps = [[-1 for _ in range(N+2)] for _ in range(N+2)] # 1,1시작, N+1도 벽(-1)으로 싸기
for i in range(1,N+1):
    for j in range(1,N+1):
        maps[i][j] = 0

scores = [0] * (P+1)
santa_state = [0] * (P+1) # -1:out 0:normal 1~2:기절
santa_pos = [[0]*2 for _ in range(P+1)]

for p in range(1, P+1):
    idx, s_r, s_c = map(int, input().split())
    santa_pos[idx][0] = s_r
    santa_pos[idx][1] = s_c
    maps[s_r][s_c] = idx # 산타 있는곳은 idx로 표시

dr = [-1,0,1,0,-1,-1,1,1] # 상우하좌 + 대각선 4방향
dc = [0,1,0,-1,-1,1,-1,1]

# 게임
for m in range(M):
    distance = [50**2+50**2] * (P+1)

    # 1. 거리 측정
    # 루돌프는 가장 가까운 산타를 향해 돌진, 가장 가까운 산타가 복수면 r이 큰 산타, r도 같으면 c가 큰 산타로 돌진
    min_d = 50**2+50**2
    min_r, min_c = 0,0
    for i in range(1,P+1):
        if santa_state[i] >= 0: # 기절도 가능
            s_r, s_c = santa_pos[i][0], santa_pos[i][1]
            d = (r_r-s_r)**2 + (r_c-s_c)**2
            if d < min_d:
                min_d = d
                min_r, min_c = s_r, s_c
            elif d == min_d:
                if min_r < s_r:
                    min_r, min_c = s_r, s_c
                elif min_r == s_r and min_c < s_c:
                    min_c = s_c

    # 2. 루돌프 이동
    # 가장 가까워지는 방향으로 1칸 돌진(상하좌우대각선)
    n_min_d = min_d
    n_r, n_c = 0,0 # 다음 루돌프 위치
    d_r, d_c = 0,0 # 루돌프 이동 방향
    for i in range(8):
        _nr, _nc = r_r + dr[i], r_c+dc[i]
        if maps[_nr][_nc] != -1:  # 벽이 아니면
            d = (_nr-min_r)**2 + (_nc-min_c)**2
            if d < n_min_d:
                n_min_d = d
                n_r, n_c = _nr, _nc
                d_r, d_c = dr[i], dc[i]
    r_r, r_c = n_r, n_c # 루돌프 이동

    # 3. 충돌 처리 + 연쇄 반응
    # 루돌프가 산타랑 충돌 -> 산타가 C만큼 점수를 얻고 날라가서 C칸 뒤에 착지
    # 다른 산타가있으면 그 산타는 1칸씩 밀려남 -> 연쇄적으로 1칸 밀려남
    # 루돌프와 충돌 후 K+1번째 턴까지 기절, (k+2)부터 정상
    if maps[r_r][r_c] != 0: # 산타랑 충돌함
        idx = maps[r_r][r_c]
        scores[idx] += C
        santa_state[idx] = 1 # 기절
        maps[r_r][r_c] = 0 # 들어갈 때 0
        n_cr, n_cc = r_r + C*d_r, r_c + C*d_c
        que = []
        que.append([idx, n_cr, n_cc])
        while que:
            idx, r, c = que.pop()
            santa_pos[idx] = [r, c]
            if 0<r<N+1 and 0<c<N+1:
                if maps[r][c] > 0: # 다른 산타가 있다...
                    _idx = maps[r][c]
                    maps[r][c] = 0
                    que.append([_idx,r+d_r,c+d_c])
                maps[r][c] = idx
            else:
                santa_state[idx] = -1 #out

    # 4. 산타 이동
    # 산타는 루돌프에게 거리가 가장 가까워지는 방향으로 1칸 이동
    # 다른 산타가 있는 곳이나 게임판 밖은 x, 움직일 수 있을 때만 이동
    # 움직일 수 있어도 루돌프에 가까워지지 않으면 이동x
    # 제일 가까워지는 방향으로 상,우,하,좌 우선순위대로 움직임 (대각선 x)
    for i in range(1, P+1):
        curr_sr, curr_sc = santa_pos[i][0], santa_pos[i][1]
        if santa_state[i] == 1:
            santa_state[i] += 1 # 한턴 더 기절
        elif santa_state[i] == 2:
            santa_state[i] = 0 # 다음 턴에 정상

        # 이 때만 이동
        elif santa_state[i] == 0:
            curr_d = (r_r-curr_sr)**2 + (r_c-curr_sc)**2
            min_d = curr_d
            new_r, new_c = curr_sr, curr_sc
            d_r, d_c = 0,0 # 이동 방향
            for j in range(4):
                n_sr, n_sc = curr_sr+dr[j], curr_sc+dc[j]
                new_d = (r_r-n_sr)**2 + (r_c-n_sc)**2
                if min_d > new_d and maps[n_sr][n_sc] == 0:
                    min_d = new_d
                    new_r, new_c = n_sr, n_sc
                    d_r, d_c = dr[j], dc[j]
            maps[curr_sr][curr_sc] = 0
            santa_pos[i] = new_r, new_c # 산타 이동
            maps[new_r][new_c] = i

            # 5. 충돌 처리
            # 산타가 움직여서 루돌프랑 충돌 -> 산타가 D만큼의 점수 얻음. 산타는 반대 방향으로 D칸 밀려남 (해당 칸에만 착지)
            # 루돌프와 충돌후 K+1번째 턴까지 기절, (k+2)부터 정상
            if new_r == r_r and new_c == r_c: #충돌함
                scores[i] += D
                santa_state[i] = 2  # 기절 - +1 후에 기절하므로 2로 기절
                maps[new_r][new_c] = 0  # 들어갈 때 0
                nnew_r, nnew_c = new_r - D*d_r, new_c - D*d_c
                que = []
                que.append([i, nnew_r, nnew_c])
                while que:
                    idx, r, c = que.pop()
                    santa_pos[idx] = [r, c]
                    if 0 < r < N + 1 and 0 < c < N + 1:
                        if maps[r][c] > 0:  # 다른 산타가 있다...
                            _idx = maps[r][c]
                            maps[r][c] = 0
                            que.append([_idx, r - d_r, c - d_c])
                        maps[r][c] = idx
                    else:
                        santa_state[idx] = -1  # out

    # 5. 생존 시 +1
    for i in range(1, P+1):
        if santa_state[i] >= 0:
            scores[i] += 1

answer  = ''
for i in range(1,P+1):
    answer += str(scores[i])+' '
print(answer)