#!/usr/bin/env python3
import torch
import numpy as np
import argparse
import sys

# --- IMPORT CÁC THƯ VIỆN CẦN THIẾT TỪ DỰ ÁN CỦA BẠN ---
# Hãy đảm bảo đường dẫn này đúng với cấu trúc thư mục của bạn
from scripts.lib import model, mcts
from scripts.lib.game import game_provider
from scripts.lib.game.tictactoe.tictactoe import TicTacToeGame
from scripts.lib.game.caro.caro_19x19 import Caro19x19

class AlphaZeroEngine:
    """
    Lớp Engine này được khởi tạo một lần duy nhất.
    Nó chứa model và logic game, sẵn sàng để tìm nước đi bất cứ lúc nào.
    """
    def __init__(self, game_type, model_path, device="cpu"):
        print("--- Đang khởi tạo AlphaZero Engine ---")
        self.device = device

        # 1. Khởi tạo môi trường game tương ứng
        self.game = self._get_game_by_type(game_type)
        print(f"-> Game logic '{type(self.game).__name__}' đã được tải.")
        print(f"   (Người chơi: Đen={self.game.player_black}, Trắng={self.game.player_white}, Trống={self.game.empty})")

        # 2. Tải model đã huấn luyện
        self.model = model.Net(input_shape=self.game.obs_shape, actions_n=self.game.action_space)
        try:
            # Sửa lại hàm map_location để tương thích với các phiên bản PyTorch
            self.model.load_state_dict(torch.load(model_path, map_location=lambda storage, loc: storage))
            self.model.to(self.device)
            self.model.eval() # Chuyển sang chế độ đánh giá (rất quan trọng!)
            print(f"-> Model từ '{model_path}' đã được tải thành công lên '{self.device}'.")
        except FileNotFoundError:
            print(f"LỖI NGHIÊM TRỌNG: Không tìm thấy file model tại '{model_path}'.")
            raise
        except Exception as e:
            print(f"LỖI khi tải model: {e}")
            raise

        # 3. Khởi tạo cây tìm kiếm MCTS (sẽ được tái sử dụng)
        self.mcts = mcts.MCTS(self.game)
        print("-> MCTS đã được khởi tạo.")
        print("--- AlphaZero Engine đã sẵn sàng! ---")

    def _get_game_by_type(self, game_type):
        """Hàm nội bộ để lấy đối tượng game dựa trên loại."""
        if game_type == 0:
            return Caro19x19()
        elif game_type == 1:
            return TicTacToeGame()
        # Thêm các game khác ở đây
        # elif game_type == 2:
        #     return Caro5x5()
        else:
            raise ValueError(f"Loại game không hợp lệ: {game_type}")

    def find_best_move(self, board_matrix, player_to_move):
        """
        Đây là hàm cốt lõi, tìm nước đi tốt nhất cho một trạng thái bàn cờ.
        Nó sẽ nhận ma trận bàn cờ và lượt đi của người chơi hiện tại.
        
        Args:
            board_matrix (np.array): Ma trận 2D biểu diễn bàn cờ.
                                     Sử dụng quy ước của game:
                                     - game.player_black (thường là 1)
                                     - game.player_white (thường là 0)
                                     - game.empty (thường là 2)
            player_to_move (int): Lượt của người chơi cần tìm nước đi (game.player_black hoặc game.player_white)

        Returns:
            tuple: (hàng, cột) của nước đi tốt nhất. Trả về (None, None) nếu không tìm thấy.
        """
        try:
            # 1. Mã hóa trạng thái bàn cờ thành định dạng mà MCTS hiểu
            # Lưu ý: MCTS làm việc với trạng thái là một số nguyên lớn (hash)
            mcts_state = self.game.encode_game_state(board_matrix.tolist())

            # 2. Chạy MCTS để tìm kiếm
            # Các giá trị này có thể được đưa ra làm tham số nếu cần
            searches = 100
            batch_size = 32
            
            # Xóa cây tìm kiếm cũ để đảm bảo không dùng lại thông tin từ lượt trước
            self.mcts.clear()
            
            self.mcts.search_batch(
                searches,
                batch_size,
                mcts_state,
                player_to_move,
                self.model,
                device=self.device
            )

            # 3. Lấy phân phối xác suất và chọn nước đi
            probs, _ = self.mcts.get_policy_value(mcts_state, tau=0)

            # 4. Lọc các nước đi không hợp lệ và chọn nước tốt nhất
            possible_moves = self.game.possible_moves(mcts_state)
            if not possible_moves:
                print("LỖI: Không còn nước đi nào trên bàn cờ.")
                return None, None

            possible_moves_mask = np.zeros_like(probs)
            possible_moves_mask[possible_moves] = 1.0
            masked_probs = probs * possible_moves_mask

            if np.sum(masked_probs) == 0:
                print("LỖI: AI không tìm thấy nước đi hợp lệ nào sau khi lọc.")
                # Nếu không còn nước nào hợp lệ theo tính toán, chọn một nước ngẫu nhiên từ các ô trống
                action = np.random.choice(possible_moves)
            else:
                action = int(np.argmax(masked_probs))

            # 5. Chuyển đổi action (số nguyên) thành tọa độ (hàng, cột)
            row, col = divmod(action, self.game.board_len)
            return row, col

        except Exception as e:
            print(f"Đã có lỗi xảy ra trong quá trình tìm nước đi: {e}")
            return None, None


# --- PHẦN API ĐỂ TÍCH HỢP ---

# Biến toàn cục để giữ engine, được khởi tạo một lần duy nhất
AI_ENGINE = None

def initialize_ai(game_type, model_path):
    """
    Hàm này phải được gọi MỘT LẦN khi bắt đầu chương trình của bạn.
    """
    global AI_ENGINE
    if AI_ENGINE is None:
        try:
            AI_ENGINE = AlphaZeroEngine(game_type, model_path)
        except Exception as e:
            print(f"KHỞI TẠO ENGINE THẤT BẠI: {e}")
            AI_ENGINE = None
    return AI_ENGINE is not None


def find_move_api(board_matrix, player_to_move):
    """
    Đây là hàm duy nhất bạn cần gọi từ game có sẵn của mình.

    Args:
        board_matrix (np.array): Trạng thái bàn cờ hiện tại.
                                 Phải theo quy ước của AI: 1=Đen, 0=Trắng, 2=Trống.
        player_to_move (int):    Lượt của người chơi cần đi (1 cho Đen, 0 cho Trắng).

    Returns:
        tuple: (hàng, cột) của nước đi. Trả về None nếu có lỗi.
    """
    if AI_ENGINE is None:
        print("Lỗi: AI Engine chưa được khởi tạo. Vui lòng gọi initialize_ai() trước.")
        return None

    return AI_ENGINE.find_best_move(board_matrix, player_to_move)


# --- KHỐI ĐỂ KIỂM TRA (TESTING) ---
if __name__ == "__main__":
    # Đây là ví dụ về cách sử dụng file này
    
    # 1. Cấu hình cho việc test
    GAME_CHOICE = 1  # 1 cho TicTacToe, 0 cho Caro
    MODEL_FILE = "path/to/your/tictactoe_model.h5" # << THAY ĐỔI ĐƯỜNG DẪN NÀY
    
    # 2. Khởi tạo AI
    if not initialize_ai(GAME_CHOICE, MODEL_FILE):
        sys.exit("Không thể khởi động AI. Thoát chương trình.")

    # 3. Tạo một bàn cờ ví dụ
    # Quy ước: 1 = Đen (X), 0 = Trắng (O), 2 = Trống
    example_board = np.array([
        [2, 1, 0],
        [2, 1, 2],
        [2, 0, 2]
    ], dtype=np.int8)

    # 4. Giả sử đến lượt người chơi Đen (1) đi
    player = 1 

    print("\n--- BẮT ĐẦU TEST TÌM NƯỚC ĐI ---")
    print("Bàn cờ hiện tại:\n", example_board)
    print(f"Tìm nước đi cho người chơi: {player} (Đen)")

    # 5. Gọi API để tìm nước đi
    move = find_move_api(example_board, player)

    # 6. In kết quả
    if move:
        row, col = move
        print(f"\n=> AI đề nghị nước đi: Hàng={row}, Cột={col}")
    else:
        print("\n=> AI không thể tìm thấy nước đi.")