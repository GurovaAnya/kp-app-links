from ..db.link import Link
from ..db.document import Document
from ..models.mapper import Mapper
from peewee import fn


class RelationsRepository:

    def __init__(self):
        self.link = Link()
        self.document = Document()
        self.mapper = Mapper()

    def get_all_links(self):
        return [self.mapper.map_edge(i.parent_id.id, i.child_id.id, i.type) for i in self.link.select()]

    def get_all_documents(self):
        return [self.mapper.map_node(i.id, i.name) for i in self.document.select()]

    def find_document_by_params(self, doc_type, authority, date, number):
        return self.document.get(Document.type == doc_type and Document.date == date
                                 and Document.authority == authority and Document.number == number)

    def find_document_by_number_date_type(self, number, date, type) -> Document:
        print("!!!!", number, date, type)
        if number is None:
            return self.document.get_or_none((Document.number.is_null()) &
                                             ((date is None) & Document.date.is_null() | (date is not None) & (Document.date == date )) &
                                               (Document.type == type.lower()))


        return self.document.get_or_none(fn.Upper(Document.number) == number.upper(),
                                         ((date is None) & Document.date.is_null() | (date is not None) & (
                                                     Document.date == date)),
                                         fn.Lower(Document.type) == type.lower())

    def save_link(self, link: Link):
        return link.save()

    def save_if_not_exists(self, link: Link):
        existing = self.link.get_or_none(Link.parent_id == link.parent_id, Link.child_id == link.child_id)
        if existing is None:
            link.save()

    def save_doc(self, doc: Document):
        if doc.number == "NONE":
            raise
        return doc.save()

    def get_document_by_id(self, id):
        return self.document.get_by_id(id)

    def get_link_by_id(self, id):
        return self.link.get_by_id(id)

    def get_child_documents(self, doc_id):
        response = Document.select(Document, Link.id, Link.start_index, Link.end_index)\
            .join(Link, on=(Document.id == Link.child_id))\
            .where(Link.parent_id == doc_id)
        return [Mapper.map_to_ref_document(q) for q in response]

    def get_parent_documents(self, doc_id):
        response = Document.select(Document, Link.id, Link.start_index, Link.end_index)\
            .join(Link, on=(Document.id == Link.parent_id))\
            .where(Link.child_id == doc_id)
        return [Mapper.map_to_ref_document(q) for q in response]

    def save_link_if_not_exists(self, db_link):
        existing = Link.get_or_none(Link.parent_id == db_link.parent_id, Link.child_id == db_link.child_id)
        if existing is None:
            Link.save(db_link)
            return

        if existing.type is None and db_link.type is not None:
            print("Апдейтим ссылку, так как появился тип")
            db_link.id = existing.id
            Link.save(db_link)

