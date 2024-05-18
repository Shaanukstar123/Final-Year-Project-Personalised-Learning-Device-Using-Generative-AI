import sqlite3
import pickle
import numpy as np
import warnings
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from rake_nltk import Rake
from transformers import pipeline
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

import os

# Suppress joblib warnings (optional)
warnings.filterwarnings("ignore", category=UserWarning, module='joblib')

# Load environment variables
load_dotenv()

# Function to generate embeddings
def textToVector(story_text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(story_text)
    return embedding

# Function to create a database connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    return conn

# Function to insert a new vector into the database
def insert_vector(conn, vector, description=None):
    serialized_vector = pickle.dumps(vector)
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
    cur.execute(create_table_sql)
    cur.execute(insert_sql, (serialized_vector, description))
    conn.commit()
    return cur.lastrowid

# Function to retrieve a vector by id
def retrieve_vector(conn, vector_id):
    cur = conn.cursor()
    cur.execute("SELECT vector FROM embeddings WHERE id=?", (vector_id,))
    data = cur.fetchone()
    if data:
        return pickle.loads(data[0])
    return None

# Function to retrieve all vectors from the database
def retrieve_all_vectors(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, vector, description FROM embeddings")
    rows = cur.fetchall()
    vectors = [pickle.loads(row[1]) for row in rows]
    descriptions = [row[2] for row in rows]
    return vectors, descriptions

# Initialize the Azure OpenAI model
def initialiseAzureModel():
    llm = AzureChatOpenAI(
        api_version=os.getenv("OPENAI_API_VERSION"),
        api_key=os.getenv("AZURE_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment="StoryGPT3"
    )
    output_parser = StrOutputParser()  # Converts output to string
    return llm, output_parser

# Generate descriptions with LangChain
def generate_cluster_descriptions(cluster_prompts):
    llm, output_parser = initialiseAzureModel()
    descriptions = []
    
    for cluster_prompt in cluster_prompts:
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are an AI that generates detailed and relevant descriptions for clusters of text. Given a representative sentence, keywords, and a summary, create a comprehensive and contextually accurate description for the cluster."),
            ("user", cluster_prompt)
        ])
        
        chain = LLMChain(llm=llm, prompt=prompt_template)
        description = chain.invoke({})
        descriptions.append(description)
    
    return descriptions

# Main script
conn = create_connection("vectors.db")

# Example text and embedding insertion
test = "It's not a flavour you might expect - her choice was haggis and black pepper. Grace wrote to the crisp company's bosses and demanded it returned to the shelves - and she got her wish! But we want to know what your favourite flavour of crisp is. Let us know in the poll further down the page, and if you don't see your top flavour included, drop it in the comments below. You can also let us know if there's a crisp flavour you're desperate to see on the shelves - maybe you'll make it your mission like Grace did? © 2024 BBC. The BBC is not responsible for the content of external sites."
embedding = textToVector(test)
vector = np.array(embedding)
vector_id = insert_vector(conn, vector, "It's not a flavour you might expect - her choice was haggis and black pepper. Grace wrote to the crisp company's bosses and demanded it returned to the shelves - and she got her wish! ...")

# Retrieve all vectors and descriptions
vectors, descriptions = retrieve_all_vectors(conn)

# Ensure unique vectors
unique_vectors, unique_indices = np.unique(vectors, axis=0, return_index=True)
unique_descriptions = [descriptions[i] for i in unique_indices]

# Adjust number of clusters
num_samples = len(unique_vectors)
num_clusters = min(5, num_samples)

# Clustering
clustering_model = KMeans(n_clusters=num_clusters)
clustering_model.fit(unique_vectors)
cluster_assignment = clustering_model.labels_

# Identify representative sentences
cluster_centers = clustering_model.cluster_centers_
representative_sentences = []

for i in range(num_clusters):
    cluster_embeddings = np.array(unique_vectors)[cluster_assignment == i]
    cluster_descriptions = np.array(unique_descriptions)[cluster_assignment == i]
    distances = np.linalg.norm(cluster_embeddings - cluster_centers[i], axis=1)
    if distances.size > 0:
        closest_index = np.argmin(distances)
        representative_sentences.append(cluster_descriptions[closest_index])

# Keyword extraction
r = Rake()
cluster_keywords = []

for i in range(num_clusters):
    cluster_descriptions = np.array(unique_descriptions)[cluster_assignment == i]
    combined_text = " ".join(cluster_descriptions)
    r.extract_keywords_from_text(combined_text)
    keywords = r.get_ranked_phrases()[:10]  # Top 10 keywords
    cluster_keywords.append(", ".join(keywords))

# Summarization
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

cluster_summaries = []

for i in range(num_clusters):
    cluster_descriptions = np.array(unique_descriptions)[cluster_assignment == i]
    combined_text = " ".join(cluster_descriptions)[:1000]
    summary = summarizer(combined_text, max_length=50, min_length=25, do_sample=False)
    cluster_summaries.append(summary[0]['summary_text'])

# Generate cluster descriptions with LangChain
cluster_prompts = [
    f"Cluster {i+1} description: Representative Sentence: {representative_sentences[i]}\nKeywords: {cluster_keywords[i]}\nSummary: {cluster_summaries[i]}"
    for i in range(num_clusters)
]

cluster_descriptions = generate_cluster_descriptions(cluster_prompts)

for i, description in enumerate(cluster_descriptions):
    print(f"Cluster {i+1} Description:\n{description}\n")