from enum import Enum, auto
from extract_json import extract_json
from filter import choice_model

ai_models = {
    "audio": "whisper-large-v3",
    "image": "qwen/qwen3.6-27b",
    "text": "openai/gpt-oss-20b",
}


print("""LLM information extraction\n

Source format :
    1. Audio (With people voice) -> mp3, wav, ...
    2. Image (With text) -> png, jpg, ...
    3. Text -> txt, docx, ...

In your message, you should have the name of the person and his age.
Example : 'Hi! My name is Claude and I'm 23 year old.

The program will extract data and return a json format.

```json
{
    "name": "The name of the person",
    "age": "The age of the person"
}
```

""")

path = input("Enter path of the file: ")
model = choice_model(path=path, models=ai_models)

print(model)
