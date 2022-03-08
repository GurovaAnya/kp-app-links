import json


class TokenMatch:

    start_index: int
    end_index: int
    text: str
    text_lemmed: str

    def __init__(self, start_index: int, end_index: int, text: str, text_lemmed: str):
        self.text = text
        self.end_index = end_index
        self.start_index = start_index
        self.text_lemmed = text_lemmed
