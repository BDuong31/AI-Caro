import numpy as np

# Định nghĩa điểm số cho các trường hợp tấn công và phòng thủ
Attack = [0, 12, 80, 300, 2500, 20000]
Defense = [0, 4, 36, 120, 1000, 8748]

# Hàm đánh giá trạng thái tại (x, y)
def EvaluatePosition(board, x, y, player, is_aggressive):
    directions = [(-1, 0), (0, -1), (-1, -1), (-1, 1)]  # Dọc, Ngang, Chéo chính, Chéo phụ
    scores = [0, 0, 0, 0]
    rows, columns = board.shape

    for idx, (dx, dy) in enumerate(directions):
        count = 0
        block_open_ends = [0, 0]

        # Hướng âm
        i, j = x + dx, y + dy
        while 0 <= i < rows and 0 <= j < columns and board[i, j] == player:
            count += 1
            i += dx
            j += dy
        if 0 <= i < rows and 0 <= j < columns and board[i, j] == 0:
            block_open_ends[0] = 1

        # Hướng dương
        i, j = x - dx, y - dy
        while 0 <= i < rows and 0 <= j < columns and board[i, j] == player:
            count += 1
            i -= dx
            j -= dy
        if 0 <= i < rows and 0 <= j < columns and board[i, j] == 0:
            block_open_ends[1] = 1

        if count == 4:
            count = 5
        elif count == 3 and sum(block_open_ends) == 2:
            count = 4

        scores[idx] = Attack[count] if is_aggressive else Defense[count]

    return sum(scores)

# Tính điểm cho máy và đối thủ
def ComputerChesses(board, x, y, player):
    return EvaluatePosition(board, x, y, player, True)

def EnemyChesses(board, x, y, player):
    opponent = -1 if player == 1 else 1
    return EvaluatePosition(board, x, y, opponent, False)

# Tổng điểm đánh giá tại ô
def Calculate(board, x, y, player):
    return ComputerChesses(board, x, y, player) + EnemyChesses(board, x, y, player)

def check_win(board, x, y, player):
    directions = [(1,0), (0,1), (1,1), (1,-1)]
    for dx, dy in directions:
        count = 1
        for dir in [1, -1]:
            i, j = x, y
            while True:
                i += dx * dir
                j += dy * dir
                if 0 <= i < board.shape[0] and 0 <= j < board.shape[1] and board[i, j] == player:
                    count += 1
                else:
                    break
        if count >= 5:
            return True
    return False

# Đánh giá toàn bộ bàn cờ
def evaluate_board(board, player):
    score = 0
    for x in range(board.shape[0]):
        for y in range(board.shape[1]):
            if board[x, y] == 0:
                score += Calculate(board, x, y, player)
    return score

# Trả về danh sách các ô trống gần ô đã đánh (cách tối đa `distance`)
def get_candidate_moves(board, distance=2):
    moves = set()
    rows, cols = board.shape
    for x in range(rows):
        for y in range(cols):
            if board[x, y] != 0:
                for dx in range(-distance, distance + 1):
                    for dy in range(-distance, distance + 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and board[nx, ny] == 0:
                            moves.add((nx, ny))
    return moves if moves else {(rows // 2, cols // 2)}  # Nếu chưa có nước nào, đánh giữa

def minimax(board, depth, maximizing_player, player, alpha, beta):
    best_move = None

    if depth == 0:
        return 0, None  # Không đánh giá toàn cục nữa

    moves = list(get_candidate_moves(board))
    # Sắp xếp nước đi theo Calculate để hỗ trợ pruning
    moves.sort(key=lambda move: -Calculate(board, move[0], move[1], player))

    if maximizing_player:
        max_eval = -float('inf')
        for x, y in moves:
            board[x, y] = player
            if check_win(board, x, y, player):
                board[x, y] = 0
                return float('inf'), (x, y)
            eval_score, _ = minimax(board, depth - 1, False, player, alpha, beta)
            board[x, y] = 0
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = (x, y)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move

    else:
        min_eval = float('inf')
        opponent = -1 if player == 1 else 1
        for x, y in moves:
            board[x, y] = opponent
            if check_win(board, x, y, opponent):
                board[x, y] = 0
                return -float('inf'), (x, y) 
            eval_score, _ = minimax(board, depth - 1, True, player, alpha, beta)
            board[x, y] = 0
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = (x, y)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move


# Tìm nước đi tối ưu
def CptFindChessMinimax(board, player, depth=2):
    _, best_move = minimax(board, depth, True, player, -float('inf'), float('inf'))
    return best_move
