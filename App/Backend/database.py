import sqlite3

def initialiseDatabase():
    conn = sqlite3.connect('data/stories.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stories (
            id INTEGER PRIMARY KEY,
            topic_id INTEGER,
            story TEXT,
            image_prompt TEXT,
            image_url TEXT,
            question TEXT
        )
    ''')
    conn.commit()
    conn.close()