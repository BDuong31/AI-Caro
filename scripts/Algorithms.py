import time
import random
from scripts.AStar import *
from scripts.Greedy import *
from scripts.MinimaxAlphaBeta import *
from scripts.engine_alphazero import *
import numpy as np

def convert_board_3d_to_2d(matrix_3d):
    """
    Chuyển đổi ma trận 3D (dùng cho model) sang 2D (dùng cho logic game).
    Hàm này giả định:
    - matrix_3d[:, :, 0] là bàn cờ của quân Đen (1).
    - matrix_3d[:, :, 1] là bàn cờ của quân Trắng (0).
    """
    # Lấy kích thước và định nghĩa các giá trị theo quy ước của AI
    rows, cols, _ = matrix_3d.shape
    EMPTY, BLACK, WHITE = 2, 1, 0

    # 1. Tạo một ma trận 2D rỗng, tất cả các ô đều là EMPTY (2)
    matrix_2d = np.full((rows, cols), EMPTY, dtype=np.int8)

    # 2. Tìm vị trí các quân Đen và điền vào ma trận 2D
    matrix_2d[matrix_3d[:, :, 0] == 1] = BLACK

    # 3. Tìm vị trí các quân Trắng và điền vào ma trận 2D
    matrix_2d[matrix_3d[:, :, 1] == 1] = WHITE
    
    return matrix_2d

def show(matrix):
    print(matrix)


def timePause(indexTime):
    start_time = time.time()
    while True:
        cur_time = time.time()
        elapsed_time = cur_time - start_time

        if elapsed_time >= indexTime:
            break


def convertSecondsToTime(seconds):
    hours = seconds // 3600
    remaining_seconds = seconds % 3600
    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60
    return int(hours), int(minutes), int(seconds)

# viết thuật toán ở đây ---------------------------------------------------------------------------------
# thuật toán gì đấy kết quả trả về là vị trí hàng nào cột số bao nhiêu


def greedy(matrix, machineRule, board_size):
    print("miniMax")
    while True:
        row, col = get_computer_move_greedy(matrix, machineRule, board_size)
        if matrix[row][col] == 0:
            return col, row
    # print(result)
    return 0, 0


def AStar(matrix, machineRule, board_size):
    print("A*")
    while True:
        row, col = CptFindChessAStar(matrix, machineRule, board_size)
        if matrix[row][col] == 0:
            return col, row
    # print(result)
    return 0, 0

def MinimaxAlphaBeta(matrix, machineRule):
    print("Minimax + Alpha-Beta")
    while True:
        move = CptFindChessMinimax(matrix, machineRule, 3)
        if move is not None:
            row, col = move
            if matrix[row][col] == 0:
                return col, row
        else:
            # Nếu không còn nước đi nào hợp lệ, trả về (0,0) hoặc None
            return 0, 0

# def AlphaZero(matrix, machineRule):
#     print("AlphaZero")
#     board2d = convert_board_3d_to_2d(matrix)
#     while True:
#         move = find_move_api(board2d, machineRule)   
#         print(move)
#         if move is not None:
#             row, col = move
#             if matrix[row][col] == 0:
#                 return col, row
#         else:
#             # Nếu không còn nước đi nào hợp lệ, trả về (0,0) hoặc None
#             return 0, 0

def AlphaZero(matrix, machineRule):
    """
    Thuật toán AlphaZero.
    Đã sửa lỗi và thêm bước chuyển đổi định dạng bàn cờ.
    """
    print("AlphaZero")
    
    # --- BƯỚC 1: Chuyển đổi bàn cờ từ quy ước của bạn (1, -1, 0) sang của AI (1, 0, 2) ---
    # Quy ước AI: 1=Đen, 0=Trắng, 2=Trống
    board_for_ai = np.full(matrix.shape, 2, dtype=np.int8) # Tạo bàn cờ rỗng (toàn số 2)
    board_for_ai[matrix == 1] = 1  # Đặt quân X (1) thành quân Đen (1)
    board_for_ai[matrix == -1] = 0 # Đặt quân O (-1) thành quân Trắng (0)
    
    # Quy ước lượt chơi của AI: 1 cho Đen, 0 cho Trắng
    ai_player_rule = 1 if machineRule == 1 else 0

    # --- BƯỚC 2: Gọi AI với dữ liệu đã được chuyển đổi ---
    move = find_move_api(board_for_ai, ai_player_rule)   
    
    if move:
        row, col = move
        # Trả về (cột, hàng) theo yêu cầu của các hàm khác
        return col, row
        
    # Trả về giá trị mặc định nếu AI không tìm được nước đi
    return 0, 0

# viết hàm khiểm tra thử ai chiến thắng nếu X thắng thì trả False nếu O thắng thì trả True nếu chưa kết thúc thỉ trả None
def checkWinner(matrix, board_size):
    if board_size > 7:
        win = 5
    elif board_size > 3:
        win = 4
    else:
        win = 3

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if j <= len(matrix[i]) - win:
                if sum(matrix[i][j+k] for k in range(win)) == win:
                    print("O wins")
                    return 1
                elif sum(matrix[i][j+k] for k in range(win)) == -win:
                    print("X wins")
                    return -1

            if i <= len(matrix) - win:
                if sum(matrix[i+k][j] for k in range(win)) == win:
                    print("O wins")
                    return 1
                elif sum(matrix[i+k][j] for k in range(win)) == -win:
                    print("X wins")
                    return -1

    # Kiểm tra đường chéo chính
    for i in range(len(matrix) - (win - 1)):
        for j in range(len(matrix[i]) - (win - 1)):
            if sum(matrix[i+k][j+k] for k in range(win)) == win:
                print("O wins")
                return 1
            elif sum(matrix[i+k][j+k] for k in range(win)) == -win:
                print("X wins")
                return -1

    # Kiểm tra đường chéo phụ
    for i in range(len(matrix) - (win - 1)):
        for j in range((win-1), len(matrix[i])):
            if sum(matrix[i+k][j-k] for k in range(win)) == win:
                print("O wins")
                return 1
            elif sum(matrix[i+k][j-k] for k in range(win)) == -win:
                print("X wins")
                return -1
    
    if not np.any(matrix == 0):
        # print("Draw")
        return 0 

