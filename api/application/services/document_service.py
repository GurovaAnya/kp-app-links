import datetime

from ..db.link import Link
from ..db.document import Document
from ..repositories.relations_repository import RelationsRepository
from ..services.lemmer import Lemmer

repo = RelationsRepository()


class DocumentService:

    def extract_doc_from_title(self, full_name, text, patterns):
        lemmer = Lemmer(full_name)
        lemmed = lemmer.get_lemmed_string()
        matched = list(lemmer.find_words(patterns))
        first_match = matched[0]
        doc = Document(name=full_name,
                       number=first_match.number,
                       date=first_match.date,
                       authority=first_match.authority,
                       type=first_match.type,
                       text=text)
        return doc

    def extract_doc_requisites_from_title(self, full_name, patterns):
        lemmer = Lemmer(full_name)
        lemmed = lemmer.get_lemmed_string()
        print(lemmed)
        matched = list(lemmer.find_words(patterns))
        first_match = matched[0]
        print("!!!!!!!!!")
        print(first_match.number)
        print("!!!!!!!!!")

        doc = Document(name=full_name,
                       number=str(first_match.number).upper(),
                       date=self.string_to_date(first_match.date),
                       type=first_match.type)
        return doc

    def lem_text(self, text):
        lemmer = Lemmer(text)
        lemmer.get_lemmed_string()
        return lemmer

    def find_links_in_lemed_text(self, lemmer, patterns):
        return list(lemmer.find_words(patterns))

    def save_matched_links(self, matched, text_id):
        for link in matched:
            child_doc = repo.find_document_by_params(doc_type=link.type, authority=link.authority, number=link.number,
                                                     date=link.date)

            db_link = Link(parent_id=text_id, child_id=child_doc, start_index=link.start_index,
                           end_index=link.end_index)
            repo.save_link(db_link)

    def string_to_date(self, string: str):
        if string is None:
            return None
        date_values = string.split(" ")
        # return DT.datetime.strptime(string, "%d %b %Y", locale="ru")
        day = int(date_values[0])
        month_list = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь',
                      'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']
        month = month_list.index(date_values[1]) + 1
        year = int(date_values[2])
        return datetime.date(year, month, day)


    # def get_month_number_from_strint(self, month_str: str):
    #     months = {
    #         "1": "январь",
    #         "2": "февраль"
    #     }