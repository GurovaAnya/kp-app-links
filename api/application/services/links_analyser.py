from .extracted_link import ExtractedLink
from .extracted_document import ExtractedDocument
from .extraction_result import ExtractionResult
from ..repositories.relations_repository import RelationsRepository
from ..models.mapper import Mapper
from ..db.BaseModel import Link, Document

relations_repository = RelationsRepository()


class LinksAnalyser:

    def save_new_docs(self, links_data: ExtractionResult) -> dict[str, Document]:
        docs_with_ids: dict[str, Document] = {}
        documents: dict[str, ExtractedDocument] = links_data.documents
        for document in documents.values():
            existing_doc = relations_repository.find_document_by_number_date_type(document.number, document.date, document.type)
            doc_id: int
            if existing_doc is None:
                document_model = Mapper.map_doc_to_model(document)
                relations_repository.save_doc(document_model)
                docs_with_ids[document.ontology_id] = document_model
            else:
                docs_with_ids[document.ontology_id] = existing_doc

        return docs_with_ids

    def map_links_to_docs(self, links_data: ExtractionResult, list_of_docs: dict[str, Document]) -> list[Link]:
        links = links_data.links
        link_models = []
        for link in links:
            link_model = Link(
                parent_id=list_of_docs[link.parent].id,
                child_id=list_of_docs[link.child].id
            )

            link_models.append(link_model)

        return link_models

    def save_links(self, links: list[Link]):
        for link in links:
            relations_repository.save_if_not_exists(link)
