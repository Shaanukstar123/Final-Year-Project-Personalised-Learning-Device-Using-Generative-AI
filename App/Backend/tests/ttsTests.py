# import pyttsx3
# engine = pyttsx3.init()
# engine.say('''Once upon a time, in the vast expanse of space, a brave spacecraft named Peregrine embarked on a mission to the Moon. It had been launched successfully onboard a powerful Vulcan rocket, carrying 
# precious scientific equipment for experiments on the lunar surface. However, Peregrine encountered a problem with its solar panels, which prevented it from generating power. The spacecraft's engineers worked 
#            tirelessly to fix the issue, but in the process, Peregrine lost a significant amount of fuel.
#            As time ticked away, Astrobotic, the private space company operating Peregrine, faced a daunting challenge. They needed to get Peregrine as close to the Moon as possible before 
#            it lost its ability to maintain a stable position towards the Sun and subsequently lost power. With their mission goals now reassessed, Astrobotic had to determine what could still be achieved 
#            in these circumstances.''')
# engine.runAndWait()

import os
from dotenv import load_dotenv
import requests

load_dotenv()

#voices
#British Daniel: onwK4e9ZLuTAKqWW03F9
#British George: JBFqnCBsd6RMkjVDRZzb
#British Dorothy: ThT5KcBeYPX3keUQqHPh
#American Brian: nPczCjzI2devNBz1zQrb
#American Rachel: 21m00Tcm4TlvDq8ikWAM

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/onwK4e9ZLuTAKqWW03F9"

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": os.getenv("ELEVENLABS_API_KEY")
}

data = {
  "text": '''Born and raised in the charming south''',
  "model_id": "eleven_monolingual_v1",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.5
  }
}

response = requests.post(url, json=data, headers=headers)
with open('audio/output.mp3', 'wb') as f:
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            f.write(chunk)

