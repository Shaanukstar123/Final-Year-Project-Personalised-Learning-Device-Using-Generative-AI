import requests
import json
import requests
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np


def getKeyWords(input_text, top_n=10):
    url = "https://portal.ayfie.com/api/keyword"
    headers = {
        "X-API-KEY": "OuopxAaSscCaWBhKxtCdinmGbXHjJnMffkmAVgYjCotghIkYlg",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    data = {
        "text": input_text,
        "top_n": top_n,
        "ngram_range": [1,1],
        "diversify": False,
        "diversity": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return list(response.json()['result'].keys())
    else:
        return response.json()

# Example
# input_text = "It is thought Australia's star striker will miss the rest of this season and potentially the start of the next, after she picked up an anterior cruciate ligament (ACL) injury whilst training with the Blues in Morocco.  An ACL injury is regarded as one of the worst to have as a footballer, with many players needing surgery and a long time on the sidelines afterwards. Some older players find it impossible to play football professionally again after having this injury.  Kerr follows in the footsteps of other unlucky players to pick up an ACL tear, including Lionesses captain Leah Williamson, her Arsenal team mate and player of the tournament at Euro 2022, Beth Mead and Vivianne Miedema, who is the Women's Super League's all-time top scorer. So why are all these superstar players getting the same injury? The answer could be a number of things, but first, what is an anterior cruciate ligament?  Our bodies are made up of bones, muscles and ligaments that help us to move.   The ligaments act as strong bits of strapping between each of the bones, holding them in place.  The anterior cruciate ligament is one of the key bits of tissue that keeps the knee bone (the patella) connected to the thigh bone (femur) above and the shinbone (tibia) below it.  But sometimes, when an athlete makes a sudden movement, stops or puts extra pressure on the knee joint, the ACL feels the pressure and can tear or snap altogether.  But there is research going on as to why this injury is more common in female footballers compared to male players.  The British Orthopaedic Association said in an article in 2023 that \"female athletes have 3-6 times higher risk of ACL injury than males\". While there is no singular explanation for this one thought is that women tend to have wider hips than men.  This can change the angle of where their knees are when a player lands on their feet during a run or jump.  Other scientific studies suggest women are also more likely to sustain injuries during certain times of their menstrual cycle.  Around the second week of the menstrual cycle, the level of hormone oestrogen in their bodies increases, which can make joints looser. This can make them more vulnerable to injury.  Another huge factor in top female players picking up this painful injury is thought to be the amount of time they spend training and playing the game, with less specialised support from physical instructors.  The intensity with which players like Sam Kerr play in the WSL is increasing, and some say more needs to be done to protect them and their bodies.  However, even the best clubs in the Women's Super League don't have the medical support that is available to top men's sides.  Dr Andrew Greene, a senior lecturer in biomechanics at the University of Roehampton, told BBC Sport that he has advised multiple WSL clubs to bring in injury prevention programmes.  \"If we can go back a step and make sure the athletes are more prepared for the intensity of a game and they are used to stopping, starting and changing direction in a controlled environment, those underlying capabilities are there and will assist in stabilising the joints and reduce the risk.\" Arsenal play-maker Beth Mead returned after just under a year on the side lines and her partner and fellow Gunners star Vivianne Miedema was also out of action for 11 months.  Lionesses captain Leah Williamson has recently returned to full training after eight months of recovery, so it is expected Sam will experience a similar time away from playing.  Kerr posted a picture on social media from hospital recently, suggesting she is seeing health specialists about her injury.  \u00a9 2024 BBC. The BBC is not responsible for the content of external sites."
# summary = summarise_text(input_text)
# print(summary)
input_text = '''Once upon a time there was an old mother pig who had three little pigs and not enough food to feed them. So when they were old enough, she sent them out into the world to seek their fortunes.

The first little pig was very lazy. He didn't want to work at all and he built his house out of straw. The second little pig worked a little bit harder but he was somewhat lazy too and he built his house out of sticks. Then, they sang and danced and played together the rest of the day.

The third little pig worked hard all day and built his house with bricks. It was a sturdy house complete with a fine fireplace and chimney. It looked like it could withstand the strongest winds.

The next day, a wolf happened to pass by the lane where the three little pigs lived; and he saw the straw house, and he smelled the pig inside. He thought the pig would make a mighty fine meal and his mouth began to water.

So he knocked on the door and said:

  Little pig! Little pig!
  Let me in! Let me in!
But the little pig saw the wolf's big paws through the keyhole, so he answered back:

  No! No! No! 
  Not by the hairs on my chinny chin chin!
Three Little Pigs, the straw houseThen the wolf showed his teeth and said:

  Then I'll huff 
  and I'll puff 
  and I'll blow your house down.
So he huffed and he puffed and he blew the house down! The wolf opened his jaws very wide and bit down as hard as he could, but the first little pig escaped and ran away to hide with the second little pig.

The wolf continued down the lane and he passed by the second house made of sticks; and he saw the house, and he smelled the pigs inside, and his mouth began to water as he thought about the fine dinner they would make.

So he knocked on the door and said:

  Little pigs! Little pigs!
  Let me in! Let me in!
But the little pigs saw the wolf's pointy ears through the keyhole, so they answered back:

  No! No! No!
  Not by the hairs on our chinny chin chin!
So the wolf showed his teeth and said:

  Then I'll huff 
  and I'll puff 
  and I'll blow your house down!
So he huffed and he puffed and he blew the house down! The wolf was greedy and he tried to catch both pigs at once, but he was too greedy and got neither! His big jaws clamped down on nothing but air and the two little pigs scrambled away as fast as their little hooves would carry them.

The wolf chased them down the lane and he almost caught them. But they made it to the brick house and slammed the door closed before the wolf could catch them. The three little pigs they were very frightened, they knew the wolf wanted to eat them. And that was very, very true. The wolf hadn't eaten all day and he had worked up a large appetite chasing the pigs around and now he could smell all three of them inside and he knew that the three little pigs would make a lovely feast.

Three Little Pigs at the Brick House

So the wolf knocked on the door and said:

  Little pigs! Little pigs!
  Let me in! Let me in!
But the little pigs saw the wolf's narrow eyes through the keyhole, so they answered back:

  No! No! No! 
  Not by the hairs on our chinny chin chin!
So the wolf showed his teeth and said:

  Then I'll huff 
  and I'll puff 
  and I'll blow your house down.
Well! he huffed and he puffed. He puffed and he huffed. And he huffed, huffed, and he puffed, puffed; but he could not blow the house down. At last, he was so out of breath that he couldn't huff and he couldn't puff anymore. So he stopped to rest and thought a bit.

But this was too much. The wolf danced about with rage and swore he would come down the chimney and eat up the little pig for his supper. But while he was climbing on to the roof the little pig made up a blazing fire and put on a big pot full of water to boil. Then, just as the wolf was coming down the chimney, the little piggy pulled off the lid, and plop! in fell the wolf into the scalding water.

So the little piggy put on the cover again, boiled the wolf up, and the three little pigs ate him for supper.
'''

test2 = '''Once upon a time there lived a poor widow and her son Jack. One day, Jack’s mother told him to sell their only cow. Jack went to the market and on the way he met a man who wanted to buy his cow. Jack asked, “What will you give me in return for my cow?” The man answered, “I will give you five magic beans!” Jack took the magic beans and gave the man the cow. But when he reached home, Jack’s mother was very angry. She said, “You fool! He took away your cow and gave you some beans!” She threw the beans out of the window. Jack was very sad and went to sleep without dinner.

The next day, when Jack woke up in the morning and looked out of the window, he saw that a huge beanstalk had grown from his magic beans! He climbed up the beanstalk and reached a kingdom in the sky. There lived a giant and his wife. Jack went inside the house and found the giant’s wife in the kitchen. Jack said, “Could you please give me something to eat? I am so hungry!” The kind wife gave him bread and some milk.

While he was eating, the giant came home. The giant was very big and looked very fearsome. Jack was terrified and went and hid inside. The giant cried, “Fee-fi-fo-fum, I smell the blood of an Englishman. Be he alive, or be he dead, I’ll grind his bones to make my bread!” The wife said, “There is no boy in here!” So, the giant ate his food and then went to his room. He took out his sacks of gold coins, counted them and kept them aside. Then he went to sleep. In the night, Jack crept out of his hiding place, took one sack of gold coins and climbed down the beanstalk. At home, he gave the coins to his mother. His mother was very happy and they lived well for sometime.

Jack and the Beanstalk Fee Fi Fo Fum!Climbed the beanstalk and went to the giant’s house again. Once again, Jack asked the giant’s wife for food, but while he was eating the giant returned. Jack leapt up in fright and went and hid under the bed. The giant cried, “Fee-fifo-fum, I smell the blood of an Englishman. Be he alive, or be he dead, I’ll grind his bones to make my bread!” The wife said, “There is no boy in here!” The giant ate his food and went to his room. There, he took out a hen. He shouted, “Lay!” and the hen laid a golden egg. When the giant fell asleep, Jack took the hen and climbed down the beanstalk. Jack’s mother was very happy with him.

After some days, Jack once again climbed the beanstalk and went to the giant’s castle. For the third time, Jack met the giant’s wife and asked for some food. Once again, the giant’s wife gave him bread and milk. But while Jack was eating, the giant came home. “Fee-fi-fo-fum, I smell the blood of an Englishman. Be he alive, or be he dead, I’ll grind his bones to make my bread!” cried the giant. “Don’t be silly! There is no boy in here!” said his wife.

The giant had a magical harp that could play beautiful songs. While the giant slept, Jack took the harp and was about to leave. Suddenly, the magic harp cried, “Help master! A boy is stealing me!” The giant woke up and saw Jack with the harp. Furious, he ran after Jack. But Jack was too fast for him. He ran down the beanstalk and reached home. The giant followed him down. Jack quickly ran inside his house and fetched an axe. He began to chop the beanstalk. The giant fell and died.

Jack and his mother were now very rich and they lived happily ever after.'''


#print(response dict keys one by one)
print(getKeyWords(input_text))


# # Preprocessing function to clean text
# def preprocess_text(text):
#     # Convert text to lowercase
#     text = text.lower()
#     # Remove punctuation
#     text = re.sub(r'[^\w\s]', '', text)
#     # Remove numbers
#     text = re.sub(r'\d+', '', text)
#     # Remove stopwords
#     stop_words = set(stopwords.words('english'))
#     text = " ".join([word for word in text.split() if word not in stop_words])
#     return text

# def get_topics(texts, num_topics=10, top_n_words=10):
#     vectorizer = CountVectorizer(max_df=0.90, min_df=1, stop_words='english')
#     dtm = vectorizer.fit_transform(texts)
#     lda = LatentDirichletAllocation(n_components=num_topics, random_state=0)
#     lda.fit(dtm)
    
#     feature_names = vectorizer.get_feature_names_out()
#     topics = {}
#     for topic_idx, topic in enumerate(lda.components_):
#         top_features_indices = topic.argsort()[:-top_n_words - 1:-1]
#         top_features = [feature_names[i] for i in top_features_indices]
#         topics[topic_idx] = top_features
    
#     return topics, lda, vectorizer

# def get_document_topics(lda_model, dtm):
#     doc_topic_distr = lda_model.transform(dtm)
#     dominant_topics = np.argmax(doc_topic_distr, axis=1)
#     return doc_topic_distr, dominant_topics

# # Example usage
# def getKeyWordsLDA(text):
#     text = [preprocess_text(book) for book in books]  # Preprocess the text
#     num_topics = len(books)
#     topics, lda_model, vectorizer = get_topics(books, num_topics=num_topics)
#     dtm = vectorizer.transform(books)
#     doc_topic_distr, dominant_topics = get_document_topics(lda_model, dtm)
#     print(topics.items())
#     return topics.items()
#     # Display topics
#     # for topic, words in topics.items():
#     #     print(f"Topic {topic}: {', '.join(words)}")

#     # Display document-topic distribution and dominant topic for each document
#     # for i, (doc_topics, topic) in enumerate(zip(doc_topic_distr, dominant_topics)):
#     #     print(f"Document {i} topic distribution: {doc_topics}")
#     #     print(f"Document {i} is dominated by Topic {topic}")

# books = [test2, input_text]
# print(getKeyWordsLDA(books))
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np
import re
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import spacy

# Ensure NLTK resources are available
import nltk
nltk.download('punkt')
nltk.download('stopwords')

nlp = spacy.load('en_core_web_sm')

COMMON_NAMES = set([
    'lily', 'alex', 'max', 'mia', 'luca', 'william', 'henry', 'francis', 'drake', 'walter', 'raleigh'
])

def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\d+', '', text)  # Remove numbers
    stop_words = set(stopwords.words('english'))
    text = " ".join([word for word in text.split() if word not in stop_words])  # Remove stopwords
    return text

def remove_names(text):
    doc = nlp(text)
    filtered_tokens = [
        token.text for token in doc if token.ent_type_ != 'PERSON' and token.text.lower() not in COMMON_NAMES
    ]
    return ' '.join(filtered_tokens)

# Split text into smaller parts
def split_text(text, chunk_size=5):
    sentences = sent_tokenize(text)
    chunks = [' '.join(sentences[i:i + chunk_size]) for i in range(0, len(sentences), chunk_size)]
    # Filter out empty chunks
    chunks = [chunk for chunk in chunks if chunk.strip() != '']
    return chunks

# LDA implementation
def get_topics(texts, num_topics=2, top_n_words=5, max_df=1.0, min_df=0.75):
    vectorizer = CountVectorizer(max_df=max_df, min_df=min_df, stop_words='english')
    dtm = vectorizer.fit_transform(texts)
    
    if len(vectorizer.get_feature_names_out()) == 0:
        raise ValueError("The vocabulary is empty. Try adjusting the max_df or min_df values.")
    
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=0)
    lda.fit(dtm)
    
    feature_names = vectorizer.get_feature_names_out()
    topics = {}
    for topic_idx, topic in enumerate(lda.components_):
        top_features_indices = topic.argsort()[:-top_n_words - 1:-1]
        top_features = [feature_names[i] for i in top_features_indices]
        topics[topic_idx] = top_features
    
    return list(topics.values())[0]  # Return the top features for the first topic

def get_document_topics(lda_model, dtm):
    doc_topic_distr = lda_model.transform(dtm)
    dominant_topics = np.argmax(doc_topic_distr, axis=1)
    return doc_topic_distr, dominant_topics

# Run LDA on the chunks
def getLdaTopics(text):
    book = preprocess_text(text)
    book = remove_names(book)
    chunks = split_text(book)
    if not chunks:  # Check if chunks are empty
        return []
    return get_topics(chunks, num_topics=1, max_df=1.0, min_df=1)


# Split the text into chunks
    chunks = split_text(book)
    return get_topics(chunks, num_topics=1, max_df=1.0, min_df=1)



# dtm = vectorizer.transform(chunks)
# doc_topic_distr, dominant_topics = get_document_topics(lda_model, dtm)
# print()

# # Display topics
# for topic, words in topics.items():
#     print(f"Topic {topic}: {', '.join(words)}")

# # Display document-topic distribution and dominant topic for each chunk
# for i, (doc_topics, topic) in enumerate(zip(doc_topic_distr, dominant_topics)):
#     print(f"Chunk {i} topic distribution: {doc_topics}")
#     print(f"Chunk {i} is dominated by Topic {topic}")
print(getLdaTopics(input_text))