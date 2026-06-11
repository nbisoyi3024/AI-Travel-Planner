# structure data for user sessions

import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join(os.getcwd(), "chat.db")


# Initialize the database and create the chat_history table if it doesn't exist
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    #only structured data
    #user table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                   email TEXT,)
                 ''')
   #itineraries table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS itineraries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        city TEXT,
        days INTEGER,
        budget TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_itinerary(user_id, city, days, budget):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO itineraries (user_id, city, days, budget)
        VALUES (?, ?, ?, ?)
    """, (user_id, city, days, budget))

    conn.commit()
    conn.close()

def get_itineraries(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
          SELECT city, days, budget
          FROM itineraries
          WHERE user_id = ?
         """, (user_id,))

    data = cursor.fetchall()
    conn.close()
    return data
    
