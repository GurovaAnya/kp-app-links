from flask import Blueprint, request, Response

from ..models.mapper import Mapper
from ..repositories.relations_repository import RelationsRepository
from ..services.document_service import DocumentService
from ..services.ontology_service import OntologyService
from ..utils.json_transformer import JsonTransformer
from ..services.implicit_links_service import ImplicitLinksService
from ..services.text_service import TextService

link_controller = Blueprint('link_controller', __name__,
                        template_folder='templates')

repo = RelationsRepository()
ontology_service = OntologyService()
document_service = DocumentService()
setting_file = open('patters.txt', 'r')
patterns = setting_file.read().splitlines()
implicit_links_service = ImplicitLinksService(patterns)
text_service = TextService()

@link_controller.route('/api/nodes')
def nodes_nice():
    documents = repo.get_all_documents()
    links = repo.get_all_links()
    imp_links = Mapper.map_impl_link_list_to_edges(implicit_links_service.get_implicit_links(0.5))
    print(imp_links)
    DAG = {
        "nodes": documents,
        "edges": links + imp_links
    }
    return JsonTransformer().transform(DAG)

@link_controller.route("/api/save_new_relation_indexes/<int:link_id>", methods=["POST"])
def save_new_relation_indexes(link_id):
    start_index = request.json["start_index"]
    end_index = request.json["end_index"]
    link = repo.get_link_by_id(link_id)
    link.start_index = start_index
    link.end_index = end_index
    repo.save_link(link)
    return Response(status=200)