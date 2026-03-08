import sqlite3
import os

# Vercel and similar serverless environments only allow writing to /tmp
if os.environ.get('VERCEL'):
    DB_PATH = '/tmp/database.db'
else:
    DB_PATH = 'database/database.db'

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            provider TEXT DEFAULT 'local',
            reset_code TEXT,
            score INTEGER DEFAULT 0
        )
    ''')
    
    # Create History table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            scan_type TEXT NOT NULL,
            content TEXT,
            risk_level TEXT,
            trust_score INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_email) REFERENCES users(email)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
