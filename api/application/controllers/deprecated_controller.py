from flask import Blueprint, Flask, request, Response

from ..repositories.relations_repository import RelationsRepository
from ..services.document_service import DocumentService
from ..utils.json_transformer import JsonTransformer

deprecated_controller = Blueprint('deprecated_controller', __name__,
                        template_folder='templates')

document_service = DocumentService()
repo = RelationsRepository()
relations_file = open('relations.txt', 'r')
relations = relations_file.read().splitlines()

@deprecated_controller.route('/api/document', methods=['POST'])
def add_document():
    document_request = request.json
    # doc = document_service.extract_doc_from_title(document_request["full_name"], document_request["text"], patterns)
    # doc = repo.save_doc(doc)
    return JsonTransformer().transform(document_request)

@deprecated_controller.route("/api/ping")
def ping():
    return Response(status=200)

@deprecated_controller.route('/api/lem/<int:text_id>')
def lem(text_id):
    text = repo.get_document_by_id(text_id).text
    lemmer = document_service.lem_text(text)
    matched = document_service.find_links_in_lemed_text(lemmer, patterns)

    result = {
        "lemmed": lemmer.lemmed_string,
        "matched": matched
    }

    document_service.save_matched_links(matched, text_id)

    return JsonTransformer().transform(result)



