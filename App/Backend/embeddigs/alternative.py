from sentence_transformers import SentenceTransformer
import numpy as np


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


model = SentenceTransformer('all-MiniLM-L6-v2')

def get_document_embeddings(texts):
    embeddings = model.encode(texts)
    return embeddings

# Example texts
books = [test, test2]
document_embeddings = get_document_embeddings(books)

from sklearn.cluster import KMeans

def cluster_embeddings(embeddings, num_clusters=2):
    clustering_model = KMeans(n_clusters=num_clusters, random_state=0)
    clustering_model.fit(embeddings)
    cluster_labels = clustering_model.labels_
    return cluster_labels

num_clusters = 2  # Adjust based on your dataset
cluster_labels = cluster_embeddings(document_embeddings, num_clusters)

for idx, label in enumerate(cluster_labels):
    print(f"Document {idx} is in cluster {label}")

from sklearn.feature_extraction.text import TfidfVectorizer

def extract_keywords_tfidf(texts, top_n=10):
    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.95, min_df=1)
    tfidf_matrix = vectorizer.fit_transform(texts)
    feature_names = vectorizer.get_feature_names_out()
    
    keywords = []
    for i in range(tfidf_matrix.shape[0]):
        tfidf_scores = tfidf_matrix[i].toarray().flatten()
        sorted_indices = np.argsort(tfidf_scores)[-top_n:]
        top_keywords = [feature_names[idx] for idx in sorted_indices]
        keywords.append(top_keywords)
    return keywords

top_keywords = extract_keywords_tfidf(books)

for idx, keywords in enumerate(top_keywords):
    print(f"Top keywords for Document {idx}: {', '.join(keywords)}")