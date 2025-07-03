import threading
import time
from scripts.Client import Client
import random

def start_game(player_name, opponent_name):
    client = Client()
    client.connect()
    
    # Đăng nhập người chơi
    print(f"Người chơi {player_name} đang đăng nhập...")
    while not client.inputUsername(player_name):
        print(f"Lỗi khi đăng ký {player_name}. Thử lại...")
        time.sleep(1)

    # Đăng nhập đối thủ
    print(f"{player_name} đang tìm đối thủ {opponent_name}...")
    while not client.inputOpponent(opponent_name):
        print(f"Không tìm thấy đối thủ {opponent_name}. Đợi đối thủ đăng nhập...")
        time.sleep(1)

    print(f"Trận đấu giữa {player_name} và {opponent_name} bắt đầu!")
    
    try:
        # Vòng lặp chính
        while True:
            row = random.randint(0, 100)
            col = random.randint(0, 100)
            client.makeMove(row, col)
            client.updateMove()
            time.sleep(0.5)
    except KeyboardInterrupt:
        print(f"{player_name} đã ngắt kết nối.")
        client.close()

def start_multiple_games(num_games):
    threads = []

    # Tạo danh sách các máy
    players = [f"máy_{i}" for i in range(1, num_games + 1)]

    for i in range(0, len(players) - 1, 2):
        # Ghép cặp 2 máy
        player1_name = f"{players[i]}"
        player2_name = f"{players[i + 1]}"

        # Tạo 2 luồng cho mỗi cặp
        thread1 = threading.Thread(target=start_game, args=(player1_name, player2_name))
        thread2 = threading.Thread(target=start_game, args=(player2_name, player1_name))

        threads.append(thread1)
        threads.append(thread2)

        # Bắt đầu các luồng
        thread1.start()
        thread2.start()

    # Đợi tất cả các thread hoàn thành
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    num_games = int(input("Nhập số lượng máy chơi đồng thời (số chẵn): "))
    if num_games % 2 != 0:
        print("Số lượng máy phải là số chẵn!")
    else:
        start_multiple_games(num_games)