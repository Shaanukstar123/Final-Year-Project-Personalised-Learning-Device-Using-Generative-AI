import sqlite3
import pickle
import numpy as np
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os
import warnings

# Suppress joblib warnings (optional)
warnings.filterwarnings("ignore", category=UserWarning, module='joblib')

# Load environment variables
load_dotenv()

# Function to generate embeddings for each word
def textToWordVectors(text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    words = text.split()
    word_embeddings = [(word, model.encode(word)) for word in words]
    return word_embeddings

# Function to create a database connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    return conn

# Function to insert a new word vector into the database
def insert_word_vector(conn, word, vector):
    serialized_vector = pickle.dumps(vector)
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS word_embeddings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT NOT NULL,
        vector BLOB NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    '''
    insert_sql = '''INSERT INTO word_embeddings(word, vector)
                    VALUES(?, ?)'''

    cur = conn.cursor()
    cur.execute(create_table_sql)
    cur.execute(insert_sql, (word, serialized_vector))
    conn.commit()
    print(f"Inserted vector for word: {word}")
    return cur.lastrowid

# Function to retrieve all word vectors from the database
def retrieve_all_word_vectors(conn):
    cur = conn.cursor()
    cur.execute("SELECT word, vector FROM word_embeddings")
    rows = cur.fetchall()
    words = [row[0] for row in rows]
    vectors = [pickle.loads(row[1]) for row in rows]
    return words, vectors

# Visualization function
def visualise_word_clusters(words, vectors, cluster_labels):
    if len(vectors) == 0:
        print("No vectors to visualize.")
        return
    
    perplexity = min(30, len(vectors) - 1)
    if perplexity <= 0:
        print("Not enough samples for t-SNE visualization.")
        return
    
    tsne = TSNE(n_components=2, perplexity=perplexity, random_state=42)
    reduced_vectors = tsne.fit_transform(vectors)
    
    plt.figure(figsize=(12, 8))
    unique_clusters = set(cluster_labels)
    
    for cluster in unique_clusters:
        indices = [i for i, c in enumerate(cluster_labels) if c == cluster]
        cluster_points = reduced_vectors[indices]
        cluster_words = [words[i] for i in indices]
        
        plt.scatter(cluster_points[:, 0], cluster_points[:, 1], label=f'Cluster {cluster}')
        
        for point, word in zip(cluster_points, cluster_words):
            plt.text(point[0], point[1], word, fontsize=9)
    
    plt.title('t-SNE Visualization of Word Clusters')
    plt.legend()
    plt.show()

# Main script
conn = create_connection("vectors.db")

# Example text and embedding insertion
test = "It's not a flavour you might expect - her choice was haggis and black pepper. Grace wrote to the crisp company's bosses and demanded it returned to the shelves - and she got her wish! But we want to know what your favourite flavour of crisp is. Let us know in the poll further down the page, and if you don't see your top flavour included, drop it in the comments below. You can also let us know if there's a crisp flavour you're desperate to see on the shelves - maybe you'll make it your mission like Grace did? © 2024 BBC. The BBC is not responsible for the content of external sites."

# Generate word embeddings
word_embeddings = textToWordVectors(test)

# Insert word embeddings into the database
for word, embedding in word_embeddings:
    insert_word_vector(conn, word, embedding)

# Retrieve all word embeddings
words, vectors = retrieve_all_word_vectors(conn)

# Ensure unique vectors
unique_vectors, unique_indices = np.unique(vectors, axis=0, return_index=True)
unique_words = [words[i] for i in unique_indices]

# Verify that the database is not empty
if len(unique_vectors) == 0 or len(unique_words) == 0:
    print("No data found in the database.")
else:
    # Adjust number of clusters
    num_samples = len(unique_vectors)
    num_clusters = min(5, num_samples)

    # Clustering
    clustering_model = KMeans(n_clusters=num_clusters)
    clustering_model.fit(unique_vectors)
    cluster_assignment = clustering_model.labels_

    visualise_word_clusters(unique_words, unique_vectors, cluster_assignment)