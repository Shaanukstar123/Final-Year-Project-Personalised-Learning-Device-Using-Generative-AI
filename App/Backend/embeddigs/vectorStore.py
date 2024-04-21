import sqlite3
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

def textToVector(story_text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(story_text)
    return embedding

def create_connection(db_file):
    """ create a database connection to the SQLite database specified by db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    return conn

def insert_vector(conn, vector, description=None):
    """ Insert a new vector into the embeddings table. If embedding table does not exist, create it."""
    serialized_vector = pickle.dumps(vector)
    # Ensure the embeddings table exists
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS embeddings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vector BLOB NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        description TEXT
    );
    '''
    insert_sql = '''INSERT INTO embeddings(vector, description)
                    VALUES(?, ?)'''

    cur = conn.cursor()
    # Create table if it does not exist
    cur.execute(create_table_sql)
    # Insert the new vector
    cur.execute(insert_sql, (serialized_vector, description))
    conn.commit()
    return cur.lastrowid

def retrieve_vector(conn, vector_id):
    """ Retrieve a vector by vector_id """
    cur = conn.cursor()
    cur.execute("SELECT vector FROM embeddings WHERE id=?", (vector_id,))
    data = cur.fetchone()
    if data:
        return pickle.loads(data[0])
    return None

conn = create_connection("vectors.db")

test = "It's not a flavour you might expect - her choice was haggis and black pepper.  Grace wrote to the crisp company's bosses and demanded it returned to the shelves - and she got her wish! But we want to know what your favourite flavour of crisp is. Let us know in the poll further down the page, and if you don't see your top flavour included, drop it in the comments below. You can also let us know if there's a crisp flavour you're desperate to see on the shelves - maybe you'll make it your mission like Grace did? \u00a9 2024 BBC. The BBC is not responsible for the content of external sites."
# Inserting a new vector
embedding = textToVector(test)
vector = np.array(embedding)
vector_id = insert_vector(conn, vector, "Sample vector")

# Retrieving a vector
retrieved_vector = retrieve_vector(conn, vector_id)
print("Retrieved Vector:", retrieved_vector)
