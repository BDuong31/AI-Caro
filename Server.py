import socket
import threading
import json
from scripts.DB import create_database, save_move

IP = '0.0.0.0'
PORT = 9999
clients = {}

def handle_client(conn, addr):
    print(f"Địa chỉ {addr} đã kết nối.")
    username = None  # Đặt trước username để sử dụng trong finally

    try:
        while True:
            data = conn.recv(1024)
            if not data:  # Kiểm tra nếu kết nối bị đóng
                break
            
            message = json.loads(data.decode())
            print(message)

            if message.get('action') == 'username' and 'username' in message:
                username = message['username']
                if username in clients:
                    conn.sendall("Tên người chơi đã tồn tại vui lòng nhập lại.".encode())
                else:
                    clients[username] = {'conn': conn, 'in_game': False, 'opponent': None, 'waiting': False}
                    conn.sendall("Tạo thành công người chơi.".encode())

            elif message.get('action') == 'delete' and 'username' in message:
                username = message['username']
                if username in clients:
                    if clients[username]['opponent']:
                        opponent = clients[username]['opponent']
                        clients[opponent]['in_game'] = False
                        clients[opponent]['opponent'] = None
                        clients[opponent]['waiting'] = True
                    del clients[username]
                    conn.sendall("Xóa người chơi thành công.".encode())
                    print(f"Người chơi {username} đã bị xóa.")
                else:
                    conn.sendall("Người chơi không tồn tại.".encode())

            else:
                opponent = message.get('opponent')

                if opponent not in clients:
                    conn.sendall("Không tìm thấy đối thủ.".encode())
                    continue

                if clients[opponent]['in_game']:
                    conn.sendall("Đối thủ đang trong trận đấu.".encode())
                    continue

                if clients[opponent]['waiting']:
                    clients[username]['in_game'] = True
                    clients[username]['opponent'] = opponent
                    clients[username]['waiting'] = False

                    clients[opponent]['in_game'] = True
                    clients[opponent]['opponent'] = username
                    clients[opponent]['waiting'] = False

                    conn.sendall(f"Đã kết nối với đối thủ {opponent}. Trò chơi bắt đầu.".encode())
                    clients[opponent]['conn'].sendall(f"Đã kết nối với đối thủ {username}. Trò chơi bắt đầu.".encode())
                    print(f"{username} và {opponent} đã bắt đầu trò chơi.")

                else:
                    clients[username]['waiting'] = True
                    conn.sendall(f"Đối thủ {opponent} đang chờ kết nối. Hãy đợi cho đến khi họ tham gia.".encode())
                
                # Xử lý trận đấu
                while True:
                    data = conn.recv(1024)
                    if not data:  # Kiểm tra nếu kết nối bị đóng
                        break
                    message = json.loads(data.decode())
                    print(message)
                    if message.get('action') == 'logout' and 'username' in message and 'opponent' in message:
                        username = message['username']
                        opponent = message['opponent']
                        if username in clients:
                            # Xóa người chơi khỏi danh sách
                            if opponent in clients:
                                opponent_conn = clients[opponent]['conn']
                                opponent_conn.sendall(json.dumps({
                                    'action': 'logout'
                                }).encode())

                                print(f"Người chơi {username} đã đăng xuất.")

                                clients[opponent]['in_game'] = False
                                clients[opponent]['opponent'] = None
                                clients[opponent]['waiting'] = True

                                del clients[username]
                        else:
                            conn.sendall("Người chơi không tồn tại.".encode())
                            
                    else:
                        opponent = message['opponent']
                        self_move = message['move']
                    
                        if opponent in clients:
                            opponent_conn = clients[opponent]['conn']

                            save_move(username, opponent, str(self_move))

                            opponent_conn.sendall(json.dumps({
                                'player': username,
                                'move': self_move
                            }).encode())
                            
                            print(f"Đã gửi dữ liệu từ người chơi {opponent} đến {username}")

    except Exception as e:
        print(f"Lỗi: {e}")

    finally:
        print(f"Người chơi {username} đã ngắt kết nối.")
        if username in clients:
            if clients[username]['opponent']:
                opponent = clients[username]['opponent']
                # Gửi thông báo đến đối thủ
                print(opponent)
                if opponent in clients and clients[opponent]['conn']:
                    clients[opponent]['conn'].sendall(json.dumps({
                        'player': username,
                        'status': 'disconnected'
                    }).encode())
                    print(f"Đã thông báo đối thủ {opponent} về việc {username} ngắt kết nối.")

                clients[opponent]['in_game'] = False
                clients[opponent]['opponent'] = None
                clients[opponent]['waiting'] = True

            del clients[username]
        conn.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen(1)
    print(f"Máy chủ hoạt động với địa chỉ: {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    create_database()
    start_server()
