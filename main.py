from filter import InputType, get_input_type
from textExtractor import TextExtractor


if __name__ == "__main__":
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
    ```""")

    path = input("Enter path of the file: ")
    file_type = get_input_type(path=path)

    match file_type:
        case InputType.AUDIO:
            print("Audio")
        case InputType.IMAGE:
            print("Image")
        case InputType.TEXT:
            print(open(path, "r+"))
