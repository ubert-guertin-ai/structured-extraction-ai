import pydantic
from extractor import Extractor


class AudioExtractor(Extractor):
    def _ask_ai(self, content: str) -> str | None:
        return super()._ask_ai(content)

    def extract_json(
        self, input: bytes | str, max_retry: int = 3
    ) -> pydantic.JsonValue:
        print(input)
        exit()

        return super().extract_json(input, max_retry)

    pass
