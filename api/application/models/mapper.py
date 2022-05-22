from ..services.extracted_document import ExtractedDocument
from ..db.document import Document
from ..models.implicit_link import ImplicitLink
from ..models.ref_document import RefDocument


class Mapper:

    @staticmethod
    def map_edge(source, target, type):
        return {
            'data':
                {
                    "source": source,
                    "target": target
                },
            'classes': str(type).lower()
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

    @staticmethod
    def map_iml_link_to_edge(link: ImplicitLink):
        return {
            'data':
                {
                    "source": link.id_1,
                    "target": link.id_2
                },
            "classes": "implicit"
        }

    @staticmethod
    def map_impl_link_list_to_edges(links: list[ImplicitLink]):
        return [Mapper.map_iml_link_to_edge(link) for link in links]

    @staticmethod
    def map_to_ref_document(query_response):
        return RefDocument(
            link_id=query_response.link.id,
            id=query_response.id,
            name=query_response.name,
            start_index=query_response.link.start_index,
            end_index=query_response.link.end_index,
        )
