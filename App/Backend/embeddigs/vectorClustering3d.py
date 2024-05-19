
import sqlite3
import pickle
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from dotenv import load_dotenv
from keyWordExtractor import getKeyWords
from keyWordExtractor import getLdaTopics
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

# Visualization function
def visualise_word_clusters_3d(words, vectors, cluster_labels):
    if len(vectors) == 0:
        print("No vectors to visualize.")
        return
    
    perplexity = 5  # Try a different value for perplexity
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
        
        ax.scatter(cluster_points[:, 0], cluster_points[:, 1], cluster_points[:, 2], label=f'Cluster {cluster}')
        
        for point, word in zip(cluster_points, cluster_words):
            ax.text(point[0], point[1], point[2], word, fontsize=9)
    
    ax.set_title('t-SNE 3D Visualization of Word Clusters')
    ax.set_xlabel('t-SNE Component 1')
    ax.set_ylabel('t-SNE Component 2')
    ax.set_zlabel('t-SNE Component 3')
    plt.legend()
    plt.show()

def vectorClustering3d(text):
    conn = create_connection("vectors.db")
    word_embeddings = textToWordVectors(text)

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

        visualise_word_clusters_3d(unique_words, unique_vectors, cluster_assignment)


test = '''
Once upon a time there was an old mother pig who had three little pigs and not enough food to feed them. So when they were old enough, she sent them out into the world to seek their fortunes.

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

# text1 = getKeyWords(test)
# text2 = getKeyWords(test2)
# text = text1 + text2
# vectorClustering3d(text)
text = getLdaTopics(test)
text = text + getLdaTopics(test2)
vectorClustering3d(text)
