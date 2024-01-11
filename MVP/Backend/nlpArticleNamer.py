import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
nltk.download('punkt')
nltk.download('stopwords')

def extract_keywords(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    keywords = [word for word in words if word.isalpha() and word not in stop_words]
    freq_dist = nltk.FreqDist(keywords)
    most_common = freq_dist.most_common(3)
    return most_common[0]

def generate_title(article):
    keywords = extract_keywords(article['content'])
    # Implement additional logic based on keywords for title generation
    return f"{keywords}: A Child's Guide"

with open('webCrawler/output.json', 'r') as file:
    data = json.load(file)
    for article in data:
        article['new_title'] = generate_title(article)

# Output the modified data with new titles
print(json.dumps(data, indent=2))
