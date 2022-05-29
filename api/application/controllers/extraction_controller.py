from flask import Blueprint, request

from ..repositories.relations_repository import RelationsRepository
from ..services.document_service import DocumentService
from ..services.ontology_service import OntologyService
from ..utils.json_transformer import JsonTransformer
from ..services.implicit_links_service import ImplicitLinksService
from ..services.text_service import TextService

extraction_controller = Blueprint('extraction_controller', __name__,
                                  template_folder='templates')

repo = RelationsRepository()
ontology_service = OntologyService()
document_service = DocumentService()
setting_file = open('patters.txt', 'r')
patterns = setting_file.read().splitlines()
relations_file = open('relations.txt', 'r')
relations = relations_file.read().splitlines()
implicit_links_service = ImplicitLinksService(patterns)
text_service = TextService()


@extraction_controller.route('/api/save_and_lem', methods=['POST'])
def save_and_lem():
    document_request = request.json
    doc = document_service.extract_doc_from_title(document_request["full_name"], patterns)
    repo.save_doc(doc)
    lemmer = document_service.lem_text(document_request["text"])
    matched = document_service.find_links_in_lemed_text(lemmer, patterns, relations)

    result = {
        "lemmed": lemmer.lemmed_string,
        "matched": matched
    }

    document_service.save_matched_links(matched, doc)
    return JsonTransformer().transform(result)


@extraction_controller.route('/api/save_and_lem/<ont_id>', methods=['POST'])
def save_and_lem_ont(ont_id):
    print('ТУТА')
    text = text_service.get_text_from_service(ont_id)
    doc = document_service.extract_doc_from_title(text["name"], patterns)
    doc.ont_id = ont_id
    existing = repo.find_document_by_number_date_type(doc.number, doc.date, doc.type)

    if existing is None:
        repo.save_doc(doc)
        existing = doc
    lemmer = document_service.lem_text(text['text'].strip())
    matched = document_service.find_links_in_lemed_text(lemmer, patterns, relations)

    result = {
        "lemmed": lemmer.lemmed_string,
        "matched": matched
    }

    document_service.save_matched_links(matched, existing.id)
    return JsonTransformer().transform(result)
