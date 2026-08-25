from audioExtractor import AudioExtractor
from filter import InputType, get_input_type
from imageExtractor import ImageExtractor
from textExtractor import TextExtractor
import base64

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

    try:
        path = input("Enter path of the file: ")
    except KeyboardInterrupt:
        print("\nBye!")
        exit()

    file_type = get_input_type(path=path)

    match file_type:
        case InputType.AUDIO:
            with open(path, "rb") as file:
                filename = path.split("/")[-1]
                binary_data = file.read()
                transcription_json = AudioExtractor(filename).extract_value(binary_data)
                json = TextExtractor().extract_value(str(transcription_json))
                print(json)
        case InputType.IMAGE:
            with open(path, "rb") as image_file:
                file_extension = path.split("/")[-1].split(".")[-1]
                binary_data = base64.b64encode(image_file.read()).decode("utf-8")
                transcription_json = ImageExtractor(file_extension).extract_value(
                    binary_data
                )
                json = TextExtractor().extract_value(str(transcription_json))
                print(json)

        case InputType.TEXT:
            text = ""

            with open(path, "r+") as f:
                for line in f:
                    text += line + "\n"

            json = TextExtractor().extract_value(text)

            print(json)
