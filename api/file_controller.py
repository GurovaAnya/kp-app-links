from io import StringIO

from flask import Blueprint, Response, request

from application.repositories.relations_repository import RelationsRepository
from application.services.document_service import DocumentService
from application.services.ontology_service import OntologyService
from application.services.implicit_links_service import ImplicitLinksService
from application.services.text_service import TextService

file_controller = Blueprint('file_controller', __name__,
                        template_folder='templates')

repo = RelationsRepository()
ontology_service = OntologyService()
document_service = DocumentService()
setting_file = open('patters.txt', 'r')
patterns = setting_file.read().splitlines()
implicit_links_service = ImplicitLinksService(patterns)
text_service = TextService()

@file_controller.route('/api/save_file', methods=['POST'])
def get_documents():
    if 'file' not in request.files:
        print('No file part')
        return Response(status=401)
    file = request.files['file']
    ontology_service.extract_from_file(file)
    return Response(status=200)


@file_controller.route("/api/ont_from_text", methods=['POST'])
def ont_from_text():
    document_request = request.json
    text = document_request["text"]
    file = StringIO(text)
    file.name = 'file.xml'
    result = ontology_service.extract_from_file(file)
    return Response(status=200)