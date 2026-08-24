import pydantic

from extractor import Extractor
import pydantic_core
from person import Person


class TextExtractor(Extractor):
    def __init__(self) -> None:
        super().__init__()

    def _ask_ai(self, content: str) -> str | None:
        chat_completion = self.client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": content}],
            temperature=1,
            response_format={"type": "json_object"},
        )

        return chat_completion.choices[0].message.content

    def extract_json(self, text: str, max_retry=3) -> pydantic.JsonValue:
        running = True
        prompt = self._make_prompt(
            role="You are an expert in text analysis.",
            mission="You should read the text in the '[TEXT]' section and extract important informations.",
            json_structure="""
            {
                "name": "The person name's (Type string or null if not found)",
                "age": "The person age's (Type number or null if not found)"
            }
            """,
            rule="""
                Don't incluse a polite closing, introduction or conclusion.
                Your response must begin with '{" and end with "}'
                If you cannot find name or age, enter "null" value         
            """,
            text=text,
        )

        json_output = "{}"
        i = 0

        while running:
            try:
                print("\033[92mExtracting data to json format...\033[0m")
                json_output = self._ask_ai(prompt)

                if json_output is None:
                    print("\033[91mError033[0m")
                    return

                print("\033[92mVerrifying json syntax...\033[0m")

                person = Person.model_validate_json(json_output)

                print("\033[92mPerfect!\033[0m")

                running = False
                return person.model_dump_json()

            except pydantic_core._pydantic_core.ValidationError as err:
                i += 1

                if i > max_retry:
                    print("\033[91mToo many trying, stopping...\033[0m")
                    return
                print(
                    f"\033[91mError in the JSON format of the LLM output. Trying again... ({i}/{max_retry}) \033[91m"
                )

                prompt = self._make_prompt(
                    role="You are an expert in JSON syntax.",
                    mission="""
                        Read the text in "[TEXT]" section. 
                        Read the text inAttend. Envoit moi en 1. Je vais t'nvoyer un screenshot du résultat  the "[WRONG JSON]", the wrong syntax.
                        Read the text in "[ERROR]" section, the message who explain how to fix the syntax error.
                    """,
                    correct_json_structure="""
                    {
                        "name": "The person name's (Type string or null if not found)",
                        "age": "The person age's (Type number or null if not found)"
                    }
                    """,
                    rule="""
                        Don't incluse a polite closing, introduction or conclusion.
                        Your response must begin with '{" and end with "}'
                        If you cannot find name or age, enter "null" value
                    """,
                    text=text,
                    error=err,
                    wrong_json=json_output,
                )
