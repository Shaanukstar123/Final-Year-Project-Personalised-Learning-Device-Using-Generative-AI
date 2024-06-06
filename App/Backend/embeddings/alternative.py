from sentence_transformers import SentenceTransformer
import numpy as np
import spacy

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_document_embeddings(texts):
    embeddings = model.encode(texts)
    return embeddings

# Example texts
# books = [test, test2, test3, test4]
# document_embeddings = get_document_embeddings(books)
COMMON_NAMES = set([
    'lily', 'alex', 'max', 'mia', 'luca', 'william', 'henry', 'francis', 'drake', 'walter', 'raleigh'
])

from sklearn.cluster import KMeans

# def cluster_embeddings(embeddings, num_clusters=2):
#     clustering_model = KMeans(n_clusters=num_clusters, random_state=0)
#     clustering_model.fit(embeddings)
#     cluster_labels = clustering_model.labels_
#     return cluster_labels

# num_clusters = 2  # Adjust based on your dataset
# cluster_labels = cluster_embeddings(document_embeddings, num_clusters)

# for idx, label in enumerate(cluster_labels):
#     print(f"Document {idx} is in cluster {label}")

from sklearn.feature_extraction.text import TfidfVectorizer
nlp = spacy.load('en_core_web_sm')
def remove_names(text):
    doc = nlp(text)
    filtered_tokens = [
        token.text for token in doc if token.ent_type_ != 'PERSON' and token.text.lower() not in COMMON_NAMES
    ]
    return ' '.join(filtered_tokens)


def extract_keywords_tfidf(texts, top_n=3):
    texts = [remove_names(text) for text in texts]
    vectorizer = TfidfVectorizer(stop_words='english', max_df=1.0, min_df=0.75)
    tfidf_matrix = vectorizer.fit_transform(texts)
    feature_names = vectorizer.get_feature_names_out()
    
    keywords = []
    for i in range(tfidf_matrix.shape[0]):
        tfidf_scores = tfidf_matrix[i].toarray().flatten()
        sorted_indices = np.argsort(tfidf_scores)[-top_n:]
        top_keywords = [feature_names[idx] for idx in sorted_indices]
        keywords.append(top_keywords)
    return keywords

# top_keywords = extract_keywords_tfidf(books)

# for idx, keywords in enumerate(top_keywords):
#     print(f"Top keywords for Document {idx}: {', '.join(keywords)}")