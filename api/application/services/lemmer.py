import re
import pymorphy2
import nltk
import string
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import WhitespaceTokenizer
from ..models.token_match import TokenMatch
from ..utils.converter import Converter


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

    def find_words(self, keywords, relations):
        print(relations)
        for (i, keyword) in enumerate(keywords):
            relation_found = False
            for (j, relation) in enumerate(relations):
                if relation_found:
                    continue
                print("LOOKING FOR: ", relation, keyword)
                iteration = re.finditer(relation + "?" + keyword, self.lemmed_string, re.IGNORECASE)
                for match in iteration:
                    print("FIND_WORDS: ", keyword, relation, match)
                    start_lemmed = match.start(0)
                    end_lemmed = match.end(0)

                    start_token_number = [idx for (idx, item) in enumerate(self.lemmed_indexes) if item[0] == start_lemmed][0]
                    start = self.text_indexes[start_token_number][0]

                    end_token_number = [idx for (idx, item) in enumerate(self.lemmed_indexes) if item[1] == end_lemmed][0]
                    end = self.text_indexes[end_token_number][1]

                    match_orig = self.text[start: end]

                    groups = match.groupdict()
                    found_relation = None
                    if groups.get("relation") is not None:
                        print("I HAVE FOUND A RELATION!: ", groups.get("relation"))
                        relation_found = True
                        found_relation = j

                    yield TokenMatch(start_index=start,
                                     end_index=end,
                                     text=match_orig,
                                     text_lemmed=match.group(0),
                                     authority=groups.get("authority"),
                                     number=groups.get("number"),
                                     date=Converter.string_to_date(groups.get("date")),
                                     doc_type=groups.get("type"),
                                     relation_type=found_relation)

    def find_words_for_title(self, keywords):
        for (i, keyword) in enumerate(keywords):
            iteration = re.finditer(keyword, self.lemmed_string, re.IGNORECASE)
            for match in iteration:
                start_lemmed = match.start(0)
                end_lemmed = match.end(0)

                start_token_number = [idx for (idx, item) in enumerate(self.lemmed_indexes) if item[0] == start_lemmed][0]
                start = self.text_indexes[start_token_number][0]

                end_token_number = [idx for (idx, item) in enumerate(self.lemmed_indexes) if item[1] == end_lemmed][0]
                end = self.text_indexes[end_token_number][1]

                match_orig = self.text[start: end]

                groups = match.groupdict()

                yield TokenMatch(start_index=start,
                                 end_index=end,
                                 text=match_orig,
                                 text_lemmed=match.group(0),
                                 authority=groups.get("authority"),
                                 number=groups.get("number"),
                                 date=Converter.string_to_date(groups.get("date")),
                                 doc_type=groups.get("type"),
                                 relation_type=None)