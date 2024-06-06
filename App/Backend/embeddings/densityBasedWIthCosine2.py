import sqlite3
import pickle
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from keyWordExtractor import getLdaTopics
from sklearn.cluster import DBSCAN
from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import cosine_distances
from sentence_transformers import SentenceTransformer
from sklearn.metrics import silhouette_score
from dotenv import load_dotenv
import warnings

# Suppress joblib warnings (optional)
warnings.filterwarnings("ignore", category=UserWarning, module='joblib')

# Load environment variables
load_dotenv()

# Function to generate embeddings for each word
def textToWordVectors(words):
    model = SentenceTransformer('Alibaba-NLP/gte-large-en-v1.5', trust_remote_code=True)
    embeddings = model.encode(words)
    return [(word, embedding) for word, embedding in zip(words, embeddings)]

# Function to create a database connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    return conn

# Function to create a new word embeddings table
def create_embeddings_table(conn):
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS word_embeddings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT NOT NULL,
        vector BLOB NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    '''
    cur = conn.cursor()
    cur.execute(create_table_sql)
    conn.commit()

# Function to insert a new word vector into the database
def insert_word_vector(conn, word, vector):
    serialized_vector = pickle.dumps(vector)
    insert_sql = '''INSERT INTO word_embeddings(word, vector)
                    VALUES(?, ?)'''
    cur = conn.cursor()
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

# Function to check vector consistency
def check_vector_shapes(vectors):
    vector_lengths = [len(vec) for vec in vectors]
    unique_lengths = set(vector_lengths)
    if len(unique_lengths) > 1:
        print(f"Inconsistent vector lengths found: {unique_lengths}")
        return False
    return True

# Function to clean the embeddings table
def clean_embeddings_table(conn):
    cur = conn.cursor()
    cur.execute("DELETE FROM word_embeddings")
    conn.commit()

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
    create_embeddings_table(conn)  # Ensure the table is created

    # Clean the table to ensure no old inconsistent data
    clean_embeddings_table(conn)
    
    word_embeddings = textToWordVectors(words)

    for word, embedding in word_embeddings:
        insert_word_vector(conn, word, embedding)

    # Retrieve all word embeddings
    words, vectors = retrieve_all_word_vectors(conn)

    # Ensure unique vectors
    if not check_vector_shapes(vectors):
        print("Vector shapes are inconsistent. Aborting clustering.")
        return

    unique_vectors, unique_indices = np.unique(vectors, axis=0, return_index=True)
    unique_words = [words[i] for i in unique_indices]

    # Verify that the database is not empty
    if len(unique_vectors) == 0 or len(unique_words) == 0:
        print("No data found in the database.")
    else:
        # Compute cosine distance matrix
        distance_matrix = cosine_distances(unique_vectors)
        
        # DBSCAN Clustering with cosine distance
        dbscan = DBSCAN(metric='precomputed', eps=0.18, min_samples=5)
        cluster_assignment = dbscan.fit_predict(distance_matrix)

        visualise_word_clusters_3d(unique_words, unique_vectors, cluster_assignment)


def compute_silhouette_scores(vectors, eps_values, min_samples):
    scores = []
    for eps in eps_values:
        dbscan = DBSCAN(metric='precomputed', eps=eps, min_samples=min_samples)
        cluster_assignment = dbscan.fit_predict(vectors)
        print(f"eps: {eps}, min_samples: {min_samples}, cluster_assignment: {np.unique(cluster_assignment)}")  # Debugging line
        if len(set(cluster_assignment)) > 1:  # Silhouette score is undefined for a single cluster
            score = silhouette_score(vectors, cluster_assignment, metric='precomputed')
            scores.append((eps, min_samples, score))
        else:
            scores.append((eps, min_samples, -1))  # -1 indicates invalid score due to single cluster
    return scores

def plot_silhouette_scores(scores):
    eps_values, min_samples_values, silhouette_scores = zip(*scores)
    silhouette_scores = np.array(silhouette_scores).reshape(len(set(eps_values)), len(set(min_samples_values)))

    fig, ax = plt.subplots(figsize=(10, 6))
    cax = ax.matshow(silhouette_scores, interpolation='nearest', cmap='viridis')
    fig.colorbar(cax)

    ax.set_xticks(np.arange(len(set(min_samples_values))))
    ax.set_yticks(np.arange(len(set(eps_values))))

    ax.set_xticklabels(np.round(list(set(min_samples_values)), 2))
    ax.set_yticklabels(np.round(list(set(eps_values)), 2))

    plt.title('Silhouette Scores for Different eps and min_samples Values')
    plt.xlabel('min_samples')
    plt.ylabel('eps')
    plt.show()

def plot_eps_vs_silhouette(scores):
    eps_values, _, silhouette_scores = zip(*scores)
    min_samples_values = list(set(_))
    if len(min_samples_values) == 1:
        plt.figure(figsize=(10, 6))
        plt.plot(eps_values, silhouette_scores, marker='o')
        plt.title('Silhouette Scores for Different eps Values (min_samples = 3)')
        plt.xlabel('eps')
        plt.ylabel('Silhouette Score')
        plt.grid(True)
        plt.show()
    else:
        print("Multiple min_samples values found, can't plot eps vs silhouette score.")

# Import stories from text file split by "Story: "
def test():
    with open('stories.txt', 'r', encoding='utf-8') as file:
        stories = file.read().split("Story:")
        storyLdaArray = []
        for story in stories:
            if story.strip():  # Ensure non-empty stories
                #print(f"Processing story: {story[:60]}...")  # Print the start of the story for context
                #ldaTopics = getLdaTopics(story)
                #themes = ["history", "world war ii", "pirates", "european history", "ships", "ocean", "adventure", "allied forces", "world war i", "electronics", "engineering", "spacex", "energy", "computers", "turing", "artificial intelligence", "robots"]
                themes = ["history", "world war ii", "pirates", "european history", "ships", "ocean", "adventure", "allied forces", "world war i", 
                                    "electronics", "engineering", "spacex", "energy", "computers", "turing", "artificial intelligence", "robots",
                                    "electricity", "circuits", "robots", "coding", "space travel", "solar system", "planets", "stars", "galaxies", 
                                    "space exploration", "rockets", "astronauts", "earth science", "nature", "animals", "plants", "ecosystems", 
                                    "environment", "climate", "weather", "dinosaurs", "prehistoric life", "fossils", "inventions", "technology", 
                                    "simple machines", "magnetism", "light", "sound", "forces", "motion", "gravity", "atoms", "molecules", "matter",
                                    "medieval history", "renaissance", "explorers", "ancient egypt", "ancient greece", "ancient rome", "vikings", 
                                    "knights", "castles", "myths", "legends", "fairy tales", "folklore", "famous inventors", "famous scientists", 
                                    "famous explorers", "famous pirates", "treasure hunting", "naval battles", "sea monsters", "marine life", 
                                    "oceans", "rivers", "lakes", "mountains", "volcanoes", "earthquakes", "deserts", "rainforests", "savannas", 
                                    "polar regions", "continents", "countries", "cultures", "languages", "arts", "music", "dance", "painting", 
                                    "sculpture", "literature", "poetry", "stories", "heroes", "heroines", "wildlife", "conservation", "recycling", 
                                    "sustainability", "renewable energy", "solar power", "wind power", "hydropower"]
                #print("number of lda topics: ", len(ldaTopics))
                #storyLdaArray.extend(ldaTopics)  # Flatten the list of LDA topics
                storyLdaArray.extend(themes)
                #print(f"Extracted LDA Topics: {ldaTopics}")

    # Cluster and visualize the words
    vectorClustering3d(storyLdaArray)

    # Evaluate silhouette scores for different eps values
    conn = create_connection("vectors.db")
    words, vectors = retrieve_all_word_vectors(conn)
    
    if not check_vector_shapes(vectors):
        print("Vector shapes are inconsistent. Aborting silhouette score evaluation.")
        return
    
    unique_vectors, unique_indices = np.unique(vectors, axis=0, return_index=True)

    # Compute cosine distance matrix
    distance_matrix = cosine_distances(unique_vectors)

    # Adjust the ranges of eps and min_samples
    eps_values = np.arange(0.1, 0.7, 0.05)
    min_samples = 3
    scores = compute_silhouette_scores(distance_matrix, eps_values, min_samples)
    
    # Plot the silhouette scores as heatmap
    plot_silhouette_scores(scores)
    
    # Plot the silhouette scores vs eps
    plot_eps_vs_silhouette(scores)

if __name__ == '__main__':
    test()
