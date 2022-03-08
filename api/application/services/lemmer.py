import re
import pymorphy2
import nltk
import string
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import WhitespaceTokenizer
from ..models.token_match import TokenMatch


class Lemmer():

    tokens = []
    lemmed_string = ""
    lemmed_indexes = []
    text_indexes = []

    def __init__(self, text):
        self.text = text
        self.text_indexes = list(WhitespaceTokenizer().span_tokenize(text))
        self.tokenize()

    def get_lemmed_string(self):
        lemmed = self.lem()
        self.lemmed_string = ' '.join(lemmed)
        self.lemmed_indexes = list(WhitespaceTokenizer().span_tokenize(self.lemmed_string))
        return self.lemmed_string

    def tokenize(self):
        self.tokens = nltk.word_tokenize(self.text)
        self.tokens = [i if (i not in string.punctuation and i != '``') else "" for i in self.tokens]
        return self.tokens

    def lem(self):
        morph = pymorphy2.MorphAnalyzer()
        tokens_norm = [morph.parse(i)[0].normal_form for i in self.tokens]
        return tokens_norm

    def find_words(self, keywords):
        print(len(self.lemmed_indexes), len(self.text_indexes))
        print(self.text_indexes)
        for (i, keyword) in enumerate(keywords):
            iteration = re.finditer(keyword, self.lemmed_string)
            for match in iteration:
                start_lemmed = match.start(0)
                end_lemmed = match.end(0)

                start_token_number = [idx for (idx, item) in enumerate(self.lemmed_indexes) if item[0] == start_lemmed][0]
                start = self.text_indexes[start_token_number][0]

                end_token_number = [idx for (idx, item) in enumerate(self.lemmed_indexes) if item[1] == end_lemmed][0]
                end = self.text_indexes[end_token_number][1]

                match_orig = self.text[start: end]
                yield TokenMatch(start, end, match_orig, match.group(0))

