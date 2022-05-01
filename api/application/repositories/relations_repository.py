from ..db.BaseModel import Link, Document
from ..models.mapper import Mapper


class RelationsRepository:

    def __init__(self):
        self.link = Link()
        self.document = Document()
        self.mapper = Mapper()

    def get_all_links(self):
        return [self.mapper.map_edge(i.parent_id.id, i.child_id.id) for i in self.link.select()]

    def get_all_documents(self):
        return [self.mapper.map_node(i.id, i.name) for i in self.document.select()]

    def find_document_by_params(self, doc_type, authority, date, number):
        return self.document.get(Document.type == doc_type and Document.date == date
                                 and Document.authority == authority and Document.number == number)

    def find_document_by_number_and_date(self, number, date) -> Document:
        return self.document.get_or_none(Document.number == number, Document.date == date)

    def save_link(self, link: Link):
        return link.save()

    def save_doc(self, doc: Document):
        return doc.save()

    def get_document_by_id(self, id):
        return self.document.get_by_id(id)
