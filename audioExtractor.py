import pydantic
from extractor import Extractor


class AudioExtractor(Extractor):
    def __init__(self, filename: str) -> None:
        self.filename = filename
        super().__init__()

    def _ask_ai(self, content: str) -> str | None:
        return super()._ask_ai(content)

    def extract_value(
        self, input: bytes | str, max_retry: int = 3
    ) -> pydantic.JsonValue | str:
        if type(input) is bytes:
            transcription = self.client.audio.transcriptions.create(
                file=(self.filename, input),
                model="whisper-large-v3",
                temperature=0,
                response_format="verbose_json",
            )
            return transcription
        else:
            return ""
