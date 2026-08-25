import pydantic
from extractor import Extractor


class ImageExtractor(Extractor):
    def __init__(self, file_extension: str) -> None:
        self.file_extension = file_extension
        super().__init__()

    def _ask_ai(self, content: str) -> str | None:
        return super()._ask_ai(content)

    def extract_value(
        self, input: str | bytes, max_retry: int = 3
    ) -> pydantic.JsonValue | str:
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Read the text in the image and write it",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{self.file_extension};base64,{input}",
                            },
                        },
                    ],
                }
            ],
            model="qwen/qwen3.6-27b",
            reasoning_effort="none",
        )

        return chat_completion.choices[0].message.content
