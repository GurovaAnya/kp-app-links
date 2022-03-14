from ..db.BaseModel import Link, Document
from ..models.edge import Mapper


class RelationsRepository:

    def __init__(self):
        self.link = Link()
        self.document = Document()
        self.mapper = Mapper()

    def get_all_links(self):
        return [self.mapper.map_edge(i.parent_id.id, i.child_id.id) for i in self.link.select()]

    def get_all_documents(self):
        return [self.mapper.map_node(i.id, i.name) for i in self.document.select()]
