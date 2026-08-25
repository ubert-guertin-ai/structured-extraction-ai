from abc import ABC, abstractmethod
import os
from groq import Groq
import pydantic


class Extractor(ABC):
    def __init__(self) -> None:
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        super().__init__()

    def _make_prompt(self, **kwargs) -> str:
        final_prompt = ""

        for key in kwargs:
            title = key.upper().replace("_", " ")
            final_prompt += f"[{title}]\n{kwargs[key]}\n\n"

        return final_prompt

    @abstractmethod
    def _ask_ai(self, content: str) -> str | None:
        pass

    @abstractmethod
    def extract_value(
        self, input: str | bytes, max_retry: int = 3
    ) -> pydantic.JsonValue | str:
        pass
