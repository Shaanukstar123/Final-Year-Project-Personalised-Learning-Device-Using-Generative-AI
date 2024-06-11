import sqlite3

def initialiseDatabase():
    conn = sqlite3.connect('data/stories.db')
    cursor = conn.cursor()
    
    # Create the stories table if it does not exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stories (
            id INTEGER PRIMARY KEY,
            topic_id INTEGER,
            story TEXT,
            image_prompt TEXT,
            image_url TEXT,
            question TEXT,
            themes TEXT
        )
    ''')

    # Create the recommendations table if it does not exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY,
            recommendations TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
