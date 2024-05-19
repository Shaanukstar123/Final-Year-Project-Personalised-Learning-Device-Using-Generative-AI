import requests
import json
import requests

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
        return response.json()['result']
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
#print(response dict keys one by one)
print(list(getKeyWords(input_text).keys()))