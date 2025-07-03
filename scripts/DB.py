import sqlite3
from datetime import datetime

# Tạo và kết nối cơ sở dữ liệu SQLite
def create_database():
    conn = sqlite3.connect('game_history.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS move_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT NOT NULL,
        opponent_name TEXT NOT NULL,
        move TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()

# Chức năng lưu nước đi
def save_move(player_name, opponent_name, move):
    conn = sqlite3.connect('game_history.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO move_history (player_name, opponent_name, move, timestamp)
    VALUES (?, ?, ?, ?)
    ''', (player_name, opponent_name, move, datetime.now()))

    conn.commit()
    conn.close()

# Chức năng lấy lịch sử nước đi
def get_move_history():
    conn = sqlite3.connect('game_history.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM move_history')
    moves = cursor.fetchall()

    for move in moves:
        print(f"ID: {move[0]}, Player: {move[1]}, Opponent: {move[2]}, Move: {move[3]}, Time: {move[4]}")

    conn.close()

# Chức năng xóa lịch sử nước đi
def clear_move_history():
    conn = sqlite3.connect('game_history.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM move_history')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    print("Lịch sử nước đi:")
    get_move_history()