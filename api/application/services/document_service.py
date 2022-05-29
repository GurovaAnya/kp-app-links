from ..db.link import Link
from ..db.document import Document
from ..repositories.relations_repository import RelationsRepository
from ..services.lemmer import Lemmer

repo = RelationsRepository()


class DocumentService:

    def extract_doc_from_title(self, full_name, patterns):
        lemmer = Lemmer(full_name)
        lemmed = lemmer.get_lemmed_string()
        matched = list(lemmer.find_words_for_title(patterns))
        print(lemmed)
        for i in matched:
            print()
        first_match = matched[0]
        number = first_match.number
        if number is not None:
            number = str(number).upper()

        doc = Document(name=full_name,
                       number=number,
                       date=first_match.date,
                       authority=first_match.authority,
                       type=first_match.type)
        return doc

    def extract_doc_requisites_from_title(self, full_name, patterns):
        lemmer = Lemmer(full_name)
        lemmed = lemmer.get_lemmed_string()
        matched = list(lemmer.find_words_for_title(patterns))
        if len(matched) == 0:
            return None
        first_match = matched[0]

        doc = Document(name=full_name,
                       number=str(first_match.number).upper(),
                       date=first_match.date,
                       type=first_match.type)
        return doc

    def lem_text(self, text):
        lemmer = Lemmer(text)
        lemmer.get_lemmed_string()
        return lemmer

    def find_links_in_lemed_text(self, lemmer, patterns, relations):
        return list(lemmer.find_words(patterns, relations))

    def save_matched_links(self, matched, text_id):
        for match in matched:
            child_doc = repo.find_document_by_number_date_type(type=match.type,
                                                               number=match.number,
                                                               date=match.date)
            print("Сохраняем ссылку: child_doc=", child_doc, ", type=", match.type, ", number= ",
                  match.number, ", date =", match.date, ", relationType = ", match.relation_type)

            if child_doc is None:
                print("Ссылка не ссылается на документ. Не сохраняем.")
                continue

            db_link = Link(parent_id=text_id,
                           child_id=child_doc.id,
                           start_index=match.start_index,
                           end_index=match.end_index,
                           type=match.relation_type)
            repo.save_link_if_not_exists(db_link)

    # def get_month_number_from_strint(self, month_str: str):
    #     months = {
    #         "1": "январь",
    #         "2": "февраль"
    #     }