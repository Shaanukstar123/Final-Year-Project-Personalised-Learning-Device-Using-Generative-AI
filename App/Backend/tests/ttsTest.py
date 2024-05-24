import os
from google.cloud import texttospeech

# Set the path to your Google Cloud service account JSON file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "keys/GoogleFypKey.json"

def text_to_speech(text):
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request
    voice = texttospeech.VoiceSelectionParams(
        language_code='en-US',
        name='en-GB-Standard-D',
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    if response.audio_content:
        return response.audio_content
    else:
        raise Exception("Failed to generate speech")

if __name__ == '__main__':
    # Example text to be converted to speech
    text = "Hello this is a test of the text to speech system. I will now narrate the first verse of... just kidding I'm not going to do that."
    
    try:
        audio_content = text_to_speech(text)
        with open('output.mp3', 'wb') as out:
            out.write(audio_content)
        print('Audio content written to file "output.mp3"')
    except Exception as e:
        print(e)
