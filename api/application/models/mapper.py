from ..services.extracted_document import ExtractedDocument
from ..db.BaseModel import Document


class Mapper:

    @staticmethod
    def map_edge(source, target):
        return {
            'data':
                {
                    "source": source,
                    "target": target
                }
        }

    @staticmethod
    def map_node(id, name):
        return {
            'data':
                {
                    "id": id,
                    'name': name
                }

        }

    @staticmethod
    def map_doc_to_model(extracted_document: ExtractedDocument) -> Document:
        return Document(
            name=extracted_document.name,
            number=extracted_document.number,
            date=extracted_document.date,
            type=extracted_document.type
        )