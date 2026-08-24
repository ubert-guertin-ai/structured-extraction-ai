import magic

ai_models = {
    "audio": "whisper-large-v3",
    "image": "qwen/qwen3.6-27b",
    "text": "openai/gpt-oss-20b",
}


def choice_model(path, models):
    mime_type = magic.from_file(path, mime=True)
    file_type = mime_type.split("/")[0]

    model = models.get(file_type)

    if model is None:
        raise ValueError("File type is'nt supported!")

    print(file_type, "detected!")
    print(f"Using {model}...")

    return model
