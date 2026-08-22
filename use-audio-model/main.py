import os
from groq import Groq

client = Groq()
filename = os.path.dirname(__file__) + "/audio.mp3"

with open(filename, "rb") as file:
    transcription = client.audio.transcriptions.create(
        file=(filename, file.read()),
        model="whisper-large-v3",
        temperature=0,
        response_format="verbose_json",
    )

    print(transcription.text)
