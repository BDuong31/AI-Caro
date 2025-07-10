import numpy as np
import heapq
import random

# Định nghĩa điểm số cho các trường hợp tấn công và phòng thủ
Attack = [0, 12, 80, 300, 2500, 20000]
Defense = [0, 4, 36, 120, 1000, 8748]

# Hàm đánh giá trạng thái của bàn cờ và tính điểm tấn công hoặc phòng thủ
def EvaluatePosition(board, x, y, player, is_aggressive, board_size):
    if board_size > 7:
        win_length = 5
    elif board_size > 3:
        win_length = 4
    else:
        win_length = 3
    directions = [(-1, 0), (0, -1), (-1, -1), (-1, 1)]  # Dọc, Ngang, Chéo chính, Chéo phụ
    scores = [0, 0, 0, 0]  # Điểm số cho 4 hướng
    rows, columns = board.shape

    for idx, (dx, dy) in enumerate(directions): # Duyệt qua từng hướng
        count = 0 # Số lượng quân cờ liên tiếp
        block_open_ends = [0, 0]  # Đếm số ô trống ở cả hai hướng

        # Kiểm tra hướng âm (đầu trước của hàng)
        i, j = x + dx, y + dy # Tính toán vị trí tiếp theo theo hướng hiện tại
        while 0 <= i < rows and 0 <= j < columns and board[i, j] == player: # Kiểm tra xem vị trí tiếp theo có hợp lệ và có quân cờ của người chơi không
            count += 1 # Số lượng quân cờ liên tiếp tăng lên
            i += dx # Cập nhật vị trí i tiếp theo theo hướng hiện tại
            j += dy # Cập nhật vị trí j tiếp theo theo hướng hiện tại
        if 0 <= i < rows and 0 <= j < columns and board[i, j] == 0: # Kiểm tra xem vị trí tiếp theo có hợp lệ và là ô trống không
            block_open_ends[0] = 1 # Đánh dấu ô trống ở đầu trước của hàng

        # Kiểm tra hướng dương (đầu sau của hàng)
        i, j = x - dx, y - dy # Tính toán vị trí tiếp theo theo hướng ngược lại
        while 0 <= i < rows and 0 <= j < columns and board[i, j] == player: # Kiểm tra xem vị trí tiếp theo có hợp lệ và có quân cờ của người chơi không
            count += 1 # Số lượng quân cờ liên tiếp tăng lên
            i -= dx # Cập nhật vị trí i tiếp theo theo hướng ngược lại
            j -= dy # Cập nhật vị trí j tiếp theo theo hướng ngược lại
        if 0 <= i < rows and 0 <= j < columns and board[i, j] == 0: # Kiểm tra xem vị trí tiếp theo có hợp lệ và là ô trống không
            block_open_ends[1] = 1 # Đánh dấu ô trống ở đầu sau của hàng

        if count == win_length-1: # 4 ô liên tiếp
            count = 5 # Đặt lại count thành 5 để đánh giá cao nhất

        if count == win_length-2 and sum(block_open_ends) == 2: # 3 ô liên tiếp và 2 ô 2 đầu trống
            count = 4 # Đặt lại count thành 4 để đánh giá cao thứ hai

        if is_aggressive: # Nếu là nước đi tấn công
            scores[idx] = Attack[count]  # Sử dụng điểm tấn công nếu aggressive 
        else: # Nếu là nước đi phòng thủ
            scores[idx] = Defense[count]  # Sử dụng điểm phòng thủ nếu không aggressive

    return sum(scores)

# Hàm tính điểm cho nước đi của máy tính
def ComputerChesses(board, x, y, player, board_size):
    return EvaluatePosition(board, x, y, player, True, board_size)

# Hàm tính điểm cho nước đi của đối thủ
def EnemyChesses(board, x, y, player, board_size):
    opponent = -1 if player == 1 else 1
    return EvaluatePosition(board, x, y, opponent, False, board_size)

# Hàm tính tổng điểm cho nước đi
def Calculate(board, x, y, player, board_size):
    return EnemyChesses(board, x, y, player, board_size) + ComputerChesses(board, x, y, player, board_size)

# Hàm tìm kiếm tốt nhất sử dụng thuật toán A*
def AStarSearch(board, player, board_size):
    open_list = []   # Danh sách chứa các nước đi tiềm năng cùng với điểm số của chúng.
    heapq.heapify(open_list) # Chuyển đổi open_list thành một heap để sử dụng thuật toán A* hiệu quả.
    closed_list = set() # Tập hợp các nước đi đã được xem xét.
    best_move = None

    # Khởi tạo với tất cả các ô trống
    for x in range(board.shape[0]): # Duyệt qua từng hàng của bàn cờ
        for y in range(board.shape[1]): # Duyệt qua từng cột của bàn cờ
            if board[x, y] == 0: 
                score = Calculate(board, x, y, player, board_size) # Tính điểm cho nước đi tại ô (x, y) 
                heapq.heappush(open_list, (-score, (x, y)))  # Dùng -score để tạo max-heap( vì phần tử nhỏ nhất luôn ở trên đỉnh của heap)

    while open_list: # Khi còn nước đi trong open_list
        score, (x, y) = heapq.heappop(open_list) # Lấy nước đi có điểm số cao nhất ra khỏi open_list 
        if (x, y) not in closed_list: # Nếu nước đi này chưa được xem xét
            closed_list.add((x, y)) # Đánh dấu nước đi này là đã xem xét
            best_move = (x, y)  # trường hợp nếu có nhiều ô bằng điểm thì lấy ô đầu tiên trong heap
            break

    return best_move # nước đi tốt nhất lấy ra từ open_list mà chưa nằm trong closed_list.

# Hàm tìm kiếm nước đi tốt nhất cho máy tính
def CptFindChessAStar(board, player, board_size):
    if np.all(board != 0):
        return None, None  # Trả về None nếu bảng cờ đầy

    # Kiểm tra xem có phải lượt đánh đầu tiên không
    if np.count_nonzero(board) == 0:
        # Nếu là lượt đánh đầu tiên, chọn ngẫu nhiên trong phạm vi 3x3 ở giữa bàn cờ
        range_x = (board.shape[0] - 3) // 2    # (19 - 3 ) // 2 = 8
        range_y = (board.shape[1] - 3) // 2    

        random_x = random.randint(range_x, range_x + 2)  # ((8,8),(10,10))
        random_y = random.randint(range_y, range_y + 2)

        return random_x, random_y

    else:
        # Nếu không phải lượt đánh đầu tiên, thực hiện tìm kiếm thông thường bằng thuật toán A*
        best_move = AStarSearch(board, player, board_size)
        return best_move
