from flask import Blueprint

from ..repositories.relations_repository import RelationsRepository
from ..services.document_service import DocumentService
from ..services.text_service import TextService
from ..services.implicit_links_service import ImplicitLinksService
from ..utils.json_transformer import JsonTransformer

document_controller = Blueprint('document_controller', __name__,
                        template_folder='templates')

document_service = DocumentService()
repo = RelationsRepository()
text_service = TextService()
setting_file = open('patters.txt', 'r')
patterns = setting_file.read().splitlines()
implicit_links_service = ImplicitLinksService(patterns)

@document_controller.route('/api/document/<int:id>')
def get_children(id):
    document = repo.get_document_by_id(id)
    text = text_service.get_text_by_id(id)
    document.text = text
    parent_for = repo.get_child_documents(id)
    child_for = repo.get_parent_documents(id)

    for child in parent_for:
        child.text = text
    for parent in child_for:
        parent_text = text_service.get_text_by_id(parent.id)
        parent.text = parent_text

    implicit = list(implicit_links_service.get_implicit_links_for_id(id, 0))

    result = {
        "document": document.__data__,
        "children": parent_for,
        "parents": child_for,
        "implicit": implicit
    }
    return JsonTransformer().transform(result)

@document_controller.route("/api/document/get_all_onts")
def get_all_onts():
    return text_service.get_all_texts_json()

@document_controller.route("/api/document/<int:id>/text")
def get_text(id):
    return text_service.get_text_by_id(id)

