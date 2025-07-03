import socket
import json
import numpy as np

IP = 'localhost'
PORT = 9999

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = None
        self.opponent = None

    def connect(self):
        try:
            self.client.connect((IP, PORT))
        except:
            return None
    
    def close(self):
        self.client.close()
    
    def isConnected(self):
        try:
            self.client.send(b'')
        except socket.error:
            print("Client hiện không kết nối với bất kỳ server nào.")
            return False
        print("Client đang kết nối đến server.")
        return True
    
    def deleteUser(self):
        if self.username is None:
            return False
        try:
            message = json.dumps({'action': 'delete', 'username': self.username})
            self.client.sendall(message.encode())
            response = self.client.recv(1024).decode()
            if response == "Xóa người chơi thành công.":
                print("Người chơi đã được xóa khỏi server.")
                self.username = None
                return True
            else:
                print("Không thể xóa người chơi.")
                return False
        except Exception as e:
            print(f"Lỗi khi gửi yêu cầu xóa: {e}")
            return False

    def inputUsername(self, username):
        self.username = username
        message = json.dumps({'action': 'username', 'username': self.username})
        self.client.sendall(message.encode())
        response = self.client.recv(1024).decode()
        if response == "Tên người chơi đã tồn tại vui lòng nhập lại.":
            print("Tên người chơi đã tồn tại vui lòng nhập lại.")
            return False
        elif response == "Tạo thành công người chơi.":
            print("Tạo thành công người chơi.")
            return True

    def inputOpponent(self, opponent):
        if opponent == self.username:
            print("Không thể nhập tên chính người chơi.")
            return False
        message = json.dumps({'action': 'opponent', 'opponent': opponent})
        self.client.sendall(message.encode())

        while True:
            response = self.client.recv(1024).decode()
            if response == "Không tìm thấy đối thủ.":
                print("Không tìm thấy đối thủ.")
                return False
            elif response == "Đối thủ đang trong trận đấu.":
                print("Đối thủ đang trong trận đấu.")
                return False
            else:
                print(f"Đối thủ {opponent} đang chờ kết nối. Hãy đợi cho đến khi họ tham gia.")
                if response == f"Đã kết nối với đối thủ {opponent}. Trò chơi bắt đầu.":
                    print(f"Đã kết nối với đối thủ {opponent}. Trò chơi bắt đầu.")
                    self.opponent = opponent
                    return True

    def makeMove(self, row, col):            
        try:
            message = {
                'action': 'move',
                'opponent': self.opponent,
                'move': [row, col]
            }
            self.client.sendall(json.dumps(message).encode())
        except ValueError:
            print("Vui lòng nhập tọa độ hợp lệ (row col).")

    def updateMove(self):
        try:
            data = self.client.recv(4096).decode()
            if not data:
                print("Kết nối đã ngắt.")
                return
            message = json.loads(data)
            
            # Xử lý thông báo đối thủ đã thoát
            if message.get('action') == 'logout':
                print("Đối thủ đã thoát. Kết thúc trò chơi.")
                return -1, -1
            
            print(f"Đối thủ {message['player']} vừa di chuyển.")
            opponent_move = np.array(message['move'])
            print(opponent_move)
            return opponent_move
        except json.JSONDecodeError as e:
            print(f"Lỗi phân tích JSON: {e}")
            return None

    def logout(self):
        if self.username is None:
            print("Không có người chơi để đăng xuất.")
            return False
        try:
            message = json.dumps({'action': 'logout', 'username': self.username, 'opponent': self.opponent})
            self.client.sendall(message.encode())
        except Exception as e:
            print(f"Lỗi khi gửi yêu cầu đăng xuất: {e}")
            return False
