import sqlite3

# Kết nối đến cơ sở dữ liệu SQLite (tạo file tts_app.db)
conn = sqlite3.connect('tts_app.db')
cursor = conn.cursor()

# Bật hỗ trợ khóa ngoại
cursor.execute('PRAGMA foreign_keys = ON')

# Tạo bảng Người dùng
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# Tạo bảng Truyện ngăn
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Stories (
        story_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# Tạo bảng Giọng Đọc
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Voices (
        voice_id INTEGER PRIMARY KEY AUTOINCREMENT,
        voice_name TEXT NOT NULL,
        language TEXT NOT NULL,
        gender TEXT CHECK(gender IN ('male', 'female', 'neutral')) NOT NULL,
        description TEXT
    )
''')

# Tạo bảng File âm thanh
cursor.execute('''
    CREATE TABLE IF NOT EXISTS AudioFiles (
        audio_id INTEGER PRIMARY KEY AUTOINCREMENT,
        story_id INTEGER NOT NULL,
        voice_id INTEGER NOT NULL,
        file_path TEXT NOT NULL,
        duration REAL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (story_id) REFERENCES Stories(story_id),
        FOREIGN KEY (voice_id) REFERENCES Voices(voice_id)
    )
''')

# Tạo bảng lịch sử chuyển đổi
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Conversions (
        conversion_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        story_id INTEGER NOT NULL,
        audio_id INTEGER NOT NULL,
        status TEXT CHECK(status IN ('pending', 'completed', 'failed')) DEFAULT 'pending',
        converted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES Users(user_id),
        FOREIGN KEY (story_id) REFERENCES Stories(story_id),
        FOREIGN KEY (audio_id) REFERENCES AudioFiles(audio_id)
    )
''')

# Tạo bảng Sở thích người dùng
cursor.execute('''
    CREATE TABLE IF NOT EXISTS UserPreferences (
        preference_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        story_id INTEGER NOT NULL,
        rating INTEGER CHECK(rating BETWEEN 1 AND 5),
        last_accessed DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES Users(user_id),
        FOREIGN KEY (story_id) REFERENCES Stories(story_id)
    )
''')

# Thêm dữ liệu mẫu vào bảng Users
cursor.executemany('''
    INSERT INTO Users (username, email, password_hash) 
    VALUES (?, ?, ?)
''', [
    ('user3', 'user3@example.com', 'hashed_password_1'),
    ('user4', 'user4@example.com', 'hashed_password_2')
])

# Thêm dữ liệu mẫu vào bảng Stories
cursor.executemany('''
    INSERT INTO Stories (title, content) 
    VALUES (?, ?)
''', [
    ('Truyện cổ tích', 'Ngày xưa, có một con mèo rất thông minh...'),
    ('Truyện cười', 'Một hôm, anh ta đi chợ và gặp một tình huống hài hước...')
])

# Thêm dữ liệu mẫu vào bảng Voices
cursor.executemany('''
    INSERT INTO Voices (voice_name, language, gender, description) 
    VALUES (?, ?, ?, ?)
''', [
    ('Nam tiếng Việt', 'vi', 'male', 'Giọng nam trầm, ấm áp'),
    ('Nữ tiếng Anh', 'en', 'female', 'Giọng nữ nhẹ nhàng, chuẩn Mỹ')
])

# Thêm dữ liệu mẫu vào bảng AudioFiles
cursor.executemany('''
    INSERT INTO AudioFiles (story_id, voice_id, file_path, duration) 
    VALUES (?, ?, ?, ?)
''', [
    (1, 1, '/audio/story1_vi.mp3', 120.5),
    (2, 2, '/audio/story2_en.mp3', 45.0)
])

# Thêm dữ liệu mẫu vào bảng Conversions
cursor.executemany('''
    INSERT INTO Conversions (user_id, story_id, audio_id, status) 
    VALUES (?, ?, ?, ?)
''', [
    (1, 1, 1, 'completed'),
    (2, 2, 2, 'completed')
])

# Thêm dữ liệu mẫu vào bảng UserPreferences
cursor.executemany('''
    INSERT INTO UserPreferences (user_id, story_id, rating) 
    VALUES (?, ?, ?)
''', [
    (1, 2, 4),
    (1, 2, 3),
    (2, 1, 5)
])

# Lưu thay đổi vào cơ sở dữ liệu
conn.commit()

# Kiểm tra dữ liệu (in danh sách Users)
cursor.execute('SELECT * FROM Users')
print("Users:")
for row in cursor.fetchall():
    print(row)


# Đóng kết nối
conn.close()
print("Cơ sở dữ liệu đã được tạo và dữ liệu mẫu đã được thêm!")