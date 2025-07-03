# File: my_alphazero_player.py
# Đặt file này vào thư mục gốc của repo `AlphaZero_Repo`.

import numpy as np
import torch
import sys
import os

# Giả định file này được đặt trong thư mục gốc của repo AlphaZero,
# các lệnh import sau sẽ hoạt động khi được gọi từ repo khác (thông qua sys.path)
from scripts.lib.model import Net
from scripts.lib.mcts import MCTS
from scripts.lib.game.caro.caro_19x19 import Caro19x19

class AlphaZeroEngine:
    """
    Lớp 'Động cơ AI' này được khởi tạo MỘT LẦN DUY NHẤT.
    Nó tải model, khởi tạo game và MCTS, sẵn sàng để tìm nước đi.
    """
    def __init__(self, model_path, device="cpu"):
        print("Đang khởi tạo AlphaZero Engine...")
        self.device = device

        # 1. Khởi tạo môi trường game từ repo
        self.game = Caro19x19()
        print(f"-> Game logic (Caro19x19) đã được tải. (Người chơi: Đen={self.game.player_black}, Trắng={self.game.player_white}, Trống={self.game.empty})")

        # 2. Tải model đã huấn luyện
        self.model = Net(input_shape=self.game.obs_shape, actions_n=self.game.action_space)
        try:
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            self.model.to(self.device)
            self.model.eval() # Chuyển sang chế độ đánh giá (rất quan trọng!)
            print(f"-> Model từ '{model_path}' đã được tải thành công lên '{self.device}'.")
        except FileNotFoundError:
            print(f"LỖI NGHIÊM TRỌNG: Không tìm thấy file model tại '{model_path}'.")
            raise

        # 3. Khởi tạo cây tìm kiếm MCTS
        self.mcts = MCTS(self.game)
        print("-> MCTS đã được khởi tạo.")
        print("AlphaZero Engine đã sẵn sàng!")

    def find_best_move(self, user_matrix, user_machine_rule):
        """
        Đây là hàm cốt lõi, tìm nước đi tốt nhất cho một bàn cờ cụ thể.
        Nó thực hiện việc chuyển đổi định dạng dữ liệu bạn yêu cầu.
        """
        # ======================================================================
        # BƯỚC A: CHUYỂN ĐỔI ĐỊNH DẠNG ĐẦU VÀO CỦA BẠN SANG ĐỊNH DẠNG CỦA GAME
        # ======================================================================
        # Định dạng của bạn: 1 (X), -1 (O), 0 (Trống)
        # Định dạng của game: 1 (Đen/X), 0 (Trắng/O), 2 (Trống)

        # Tạo một ma trận rỗng theo định dạng của game
        game_matrix = np.full((19, 19), self.game.empty, dtype=np.int8)
        
        # Duyệt qua ma trận đầu vào và điền vào ma trận game
        game_matrix[user_matrix == 1] = self.game.player_black  # 1 -> 1
        game_matrix[user_matrix == -1] = self.game.player_white # -1 -> 0
        # Các ô còn lại mặc định đã là `self.game.empty` (giá trị 2)
        print(game_matrix)

        # Chuyển đổi lượt của máy từ định dạng của bạn (1, -1) sang của game (1, 0)
        game_player_code = self.game.player_black if user_machine_rule == 1 else self.game.player_white

        # Mã hóa ma trận game thành một số nguyên lớn mà MCTS sử dụng làm key
        mcts_state = self.game.encode_game_state(game_matrix.tolist())
        
        # ======================================================================
        # BƯỚC B: CHẠY MCTS ĐỂ TÌM NƯỚC ĐI TỐT NHẤT
        # ======================================================================
        self.mcts.search_batch(
            100, 
            32, 
            mcts_state, 
            game_player_code, 
            self.model,
            device=self.device
        )

        # Lấy phân phối xác suất nước đi (policy) sau khi tìm kiếm
        probs, _ = self.mcts.get_policy_value(mcts_state, tau=0)
        
        # ======================================================================
        # BƯỚC C: XỬ LÝ ĐẦU RA VÀ TRẢ VỀ THEO ĐỊNH DẠNG BẠN YÊU CẦU
        # ======================================================================
        # Lặp để đảm bảo trả về nước đi hợp lệ
        while True:
            # Chọn nước đi có xác suất cao nhất
            action = int(np.argmax(probs))
            
            # Chuyển đổi 'action' (một số từ 0-360) thành tọa độ (hàng, cột)
            row, col = divmod(action, self.game.board_len)

            # Kiểm tra lại trên ma trận GỐC của bạn xem ô có trống không
            if user_matrix[row, col] == 0:
                # Nếu trống, đây là nước đi hợp lệ, trả về (hàng, cột)
                return row, col
            else:
                # Nếu không, AI đã tính toán sai, loại bỏ nước đi này và tìm cái tốt nhất tiếp theo
                print(f"CẢNH BÁO: AI đã chọn ô đã đánh ({row},{col}). Đang tìm lựa chọn khác.")
                probs[action] = -1 # Đánh dấu là không thể chọn
                if np.all(probs < 0): # Nếu không còn nước nào để chọn
                    print("LỖI: AI không tìm thấy nước đi hợp lệ nào.")
                    return None, None 

# --- PHẦN KHỞI TẠO TOÀN CỤC ---
# Chỉ chạy một lần duy nhất khi file này được import lần đầu.
MODEL_FILE_PATH = "/Users/bduong/Documents/tictactoe-fititvaa/scripts/lib/saves/caro_exp_01/best_036_03280.dat"
AI_ENGINE = None
try:
    AI_ENGINE = AlphaZeroEngine(MODEL_FILE_PATH)
except Exception as e:
    print(f"Không thể khởi tạo AI Engine. Lỗi: {e}")

def findAlphaZero(matrix, machineRule):
    """
    Hàm API cuối cùng, có đầu vào và đầu ra đúng như bạn yêu cầu.
    """
    if AI_ENGINE is None:
        print("Lỗi: AI Engine chưa được khởi tạo thành công.")
        return 0, 0 # Trả về giá trị mặc định nếu engine lỗi
    
    # Gọi hàm xử lý chính của engine
    row, col = AI_ENGINE.find_best_move(matrix, machineRule)
    
    if row is None: # Xử lý trường hợp không tìm được nước đi
        return 0, 0
        
    # Trả về (cột, hàng) theo đúng định dạng bạn muốn
    return col, row