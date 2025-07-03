import time
import random
from scripts.AStar import *
from scripts.Greedy import *
from scripts.MinimaxAlphaBeta import *
from scripts.alphazero_player import *


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

def AlphaZero(matrix, machineRule):
    print("AlphaZero")
    while True:
        move = findAlphaZero(matrix, machineRule)
        if move is not None:
            row, col = move
            if matrix[row][col] == 0:
                return col, row
        else:
            # Nếu không còn nước đi nào hợp lệ, trả về (0,0) hoặc None
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

