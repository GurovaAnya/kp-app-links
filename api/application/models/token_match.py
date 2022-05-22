class TokenMatch:

    start_index: int
    end_index: int
    text: str
    text_lemmed: str
    authority: str
    number: str
    date: str
    type: str

    def __init__(self, start_index: int, end_index: int, text: str,
                 text_lemmed: str, authority: str, number: str, date: str, doc_type: str, relation_type):
        self.text = text
        self.end_index = end_index
        self.start_index = start_index
        self.text_lemmed = text_lemmed
        self.authority = authority
        self.number = number
        self.date = date
        self.type = doc_type
        self.relation_type = relation_type
