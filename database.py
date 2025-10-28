import sqlite3
import os

DB_PATH = 'attendance.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Users table: id, name, face_encoding (stored as BLOB for simplicity)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            face_encoding BLOB
        )
    ''')
    
    # Attendance table: id, user_id, timestamp
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_user(name, face_encoding):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO users (name, face_encoding) VALUES (?, ?)', (name, face_encoding))
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return user_id

def get_all_encodings():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT name, face_encoding FROM users')
    results = cursor.fetchall()
    conn.close()
    return {name: encoding for name, encoding in results}

def mark_attendance(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO attendance (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()

def get_attendance_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT u.name, a.timestamp 
        FROM attendance a 
        JOIN users u ON a.user_id = u.id 
        ORDER BY a.timestamp DESC
    ''')
    results = cursor.fetchall()
    conn.close()
    return results