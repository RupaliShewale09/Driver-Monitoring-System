import sqlite3
from datetime import datetime
from utils import resource_path

drowsinessDB = resource_path("db/drowsiness_logs.db")

class DrowsinessDatabase:
    def __init__(self, db_name=drowsinessDB):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.table_name = self.get_today_table_name()
        self.create_events_table()
        self.create_table_for_today()

    def get_today_table_name(self):
        today = datetime.now().strftime("%Y_%m_%d")
        return f"drowsiness_{today}"
    
    def create_events_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS drowsiness_events (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_email TEXT,
                                timestamp TEXT,
                                ear REAL,
                                mar REAL,
                                yaw_angle REAL,
                                status TEXT)''')
        self.conn.commit()
            
    def create_table_for_today(self):
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.table_name} (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_email TEXT,
                                timestamp TEXT,
                                ear REAL,
                                mar REAL,
                                yaw_angle REAL,
                                status TEXT)''')
        self.conn.commit()
        
    def log_drowsiness(self, user_email, ear, mar, yaw_angle, status):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO drowsiness_events (user_email, timestamp, ear, mar, yaw_angle, status) VALUES (?, ?, ?, ?, ?, ?)",
                            (user_email, timestamp, ear, mar, yaw_angle, status))
        self.conn.commit()        
        self.cursor.execute(f"INSERT INTO {self.table_name} (user_email, timestamp, ear, mar, yaw_angle, status) VALUES (?, ?, ?, ?, ?, ?)",
                            (user_email, timestamp, ear, mar, yaw_angle, status))
        self.conn.commit()

    def fetch_today_logs(self, user_email):
        self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE user_email = ?", (user_email,))
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()
