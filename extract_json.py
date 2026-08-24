import os
from groq import Groq
from pydantic import BaseModel, PositiveInt
import pydantic_core


class Person(BaseModel):
    name: str | None = None
    age: PositiveInt | None = None


client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


def get_prompt(msg):
    return (
        """
        [ROLE]
        You are an expert in text analysis.

        [MISSION]
        You should read the text in the "[TEXT]" section and extract important informations.

        [JSON STRUCTURE]
        {
        "name": "The person name's (Type string or null if not found)",
        "age": "The person age's (Type number or null if not found)"
        }

        [RULE]
        Don't incluse a polite closing, introduction or conclusion.
        Your response must begin with '{" and end with "}'
        If you cannot find name or age, enter "null" value

        [TEXT]
    """
        + msg
    )


def get_debug_prompt(error_msg, wrong_json, text):

    debug_text = f"""
        [TEXT]
        {text}

        [ERROR]
        {error_msg}

        [WRONG JSON]
        {wrong_json}
    """

    return (
        """
        [ROLE]
        You are an expert in JSON syntax.

        [MISSION]
        Read the text in "[TEXT]" section. 
        Read the text inAttend. Envoit moi en 1. Je vais t'nvoyer un screenshot du résultat  the "[WRONG JSON]", the wrong syntax.
        Read the text in "[ERROR]" section, the message who explain how to fix the syntax error.

        [THE CORRECT JSON STRUCTURE]
        {
        "name": "The person name's (Type string or null if not found)",
        "age": "The person age's (Type number or null if not found)"
        }

        [RULE]
        Don't incluse a polite closing, introduction or conclusion.
        Your response must begin with '{" and end with "}'
        If you cannot find name or age, enter "null" value
    """
        + debug_text
    )


def ask_ai(msg):
    chat_completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": msg}],
        temperature=1,
        response_format={"type": "json_object"},
    )

    return chat_completion.choices[0].message.content


def extract_json(text):
    running = True
    prompt = get_prompt(text)
    json_output = "{}"

    while running:
        try:
            json_output = ask_ai(prompt)

            if json_output is None:
                raise Exception("Result is None!")

            person = Person.model_validate_json(json_output)
            running = False
            return person.model_dump_json()
        except pydantic_core._pydantic_core.ValidationError as err:
            print("Error in the JSON format of the LLM output ! Trying again...")
            print(err, json_output)
            prompt = get_debug_prompt(err, json_output, text)
