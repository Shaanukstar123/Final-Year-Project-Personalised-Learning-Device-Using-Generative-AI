import sqlite3
import pickle
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sentence_transformers import SentenceTransformer
from keyWordExtractor import getLdaTopics
from alternative import extract_keywords_tfidf
from sklearn.cluster import DBSCAN
from sklearn.manifold import TSNE
from dotenv import load_dotenv
import warnings

# Suppress joblib warnings (optional)
warnings.filterwarnings("ignore", category=UserWarning, module='joblib')

# Load environment variables
load_dotenv()

# Function to generate embeddings for each word
def textToWordVectors(words):
    model = SentenceTransformer('all-MiniLM-L6-v2')
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

def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\d+', '', text)  # Remove numbers
    stop_words = set(stopwords.words('english'))
    text = " ".join([word for word in text.split() if word not in stop_words])  # Remove stopwords
    return text

# Split text into smaller parts
def split_text(text, chunk_size=5):
    sentences = sent_tokenize(text)
    chunks = [' '.join(sentences[i:i + chunk_size]) for i in range(0, len(sentences), chunk_size)]
    return chunks

# Preprocess and split the texts

# Visualization function
def visualise_word_clusters_3d(words, vectors, cluster_labels):
    if len(vectors) == 0:
        print("No vectors to visualize.")
        return
    
    vectors = np.array(vectors)  # Convert to numpy array
    perplexity = min(5, len(vectors) - 1)  # Adjust perplexity if necessary
    learning_rate = 200  # Default learning rate
    n_iter = 1000  # Number of iterations

    tsne = TSNE(n_components=3, perplexity=perplexity, learning_rate=learning_rate, n_iter=n_iter, random_state=42)
    reduced_vectors = tsne.fit_transform(vectors)
    
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    unique_clusters = set(cluster_labels)
    
    for cluster in unique_clusters:
        indices = [i for i, c in enumerate(cluster_labels) if c == cluster]
        cluster_points = reduced_vectors[indices]
        cluster_words = [words[i] for i in indices]
        
        if cluster == -1:
            continue
            color = 'k'  # Noise points colored black
            label = 'Noise'
        else:
            color = None  # Use default coloring
            label = f'Cluster {cluster}'
            # Plot names for clustered points only
            for point, word in zip(cluster_points, cluster_words):
                ax.text(point[0], point[1], point[2], word, fontsize=9)

        ax.scatter(cluster_points[:, 0], cluster_points[:, 1], cluster_points[:, 2], label=label, color=color)
    
    ax.set_title('t-SNE 3D Visualization of Word Clusters')
    ax.set_xlabel('t-SNE Component 1')
    ax.set_ylabel('t-SNE Component 2')
    ax.set_zlabel('t-SNE Component 3')
    plt.legend()
    plt.show()

def vectorClustering3d(words):
    conn = create_connection("vectors.db")
    
    word_embeddings = textToWordVectors(words)

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
        # DBSCAN Clustering
        dbscan = DBSCAN(eps=0.85, min_samples=2)
        cluster_assignment = dbscan.fit_predict(unique_vectors)

        visualise_word_clusters_3d(unique_words, unique_vectors, cluster_assignment)

#import stories from text file split by "story: "
with open('stories.txt', 'r') as file:
    stories = file.read().split("Story:")
    storyLdaArray = []
    for story in stories:
        if story.strip():  # Ensure non-empty stories
            print(f"Processing story: {story[:60]}...")  # Print the start of the story for context
            ldaTopics = extract_keywords_tfidf([story])  # Pass the story as a list
            ldaTopics_flat = [keyword for sublist in ldaTopics for keyword in sublist]  # Flatten the list of lists
            storyLdaArray.extend(ldaTopics_flat)  # Add the extracted keywords to the array
            print(f"Extracted Keywords: {ldaTopics_flat}")
            # ldaTopics = getLdaTopics(story)
            storyLdaArray.extend(ldaTopics)  # Flatten the list of LDA topics
            print(f"Extracted LDA Topics: {ldaTopics}")

# Cluster and visualize the words
#vectorClustering3d(storyLdaArray)