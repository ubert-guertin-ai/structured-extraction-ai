import magic
from enum import Enum, auto


class InputType(Enum):
    TEXT = auto()
    AUDIO = auto()
    IMAGE = auto()


def get_input_type(path) -> InputType | None:
    mime_type = magic.from_file(path, mime=True)
    file_type = mime_type.split("/")[0].upper()

    try:
        input_type = InputType[file_type]
    except KeyError:
        return None

    return input_type
