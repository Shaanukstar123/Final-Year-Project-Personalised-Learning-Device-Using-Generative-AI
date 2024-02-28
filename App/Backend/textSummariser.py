import requests
import json
import requests

def summarise_text(input_text, min_length=20, max_length=50, language="auto"):
    url = "https://portal.ayfie.com/api/summarize"
    headers = {
        "X-API-KEY": "OuopxAaSscCaWBhKxtCdinmGbXHjJnMffkmAVgYjCotghIkYlg",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    data = {
        "language": language,
        "text": input_text,
        "min_length": min_length,
        "max_length": max_length
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