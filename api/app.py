from io import StringIO

from flask import Flask, request, Response
from flask_cors import CORS

from application.repositories.relations_repository import RelationsRepository
from application.services.document_service import DocumentService
from application.services.ontology_service import OntologyService
from application.utils.json_transformer import JsonTransformer
from application.services.implicit_links_service import ImplicitLinksService
from application.models.mapper import Mapper

app = Flask(__name__)
app.secret_key = "super secret key"
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

repo = RelationsRepository()
ontology_service = OntologyService()
document_service = DocumentService()
setting_file = open('settings/patters.txt', 'r')
patterns = setting_file.read().splitlines()
implicit_links_service = ImplicitLinksService(patterns)


@app.route('/api/document', methods=['POST'])
def add_document():
    document_request = request.json
    doc = document_service.extract_doc_from_title(document_request["full_name"], document_request["text"], patterns)
    doc = repo.save_doc(doc)
    return JsonTransformer().transform(doc)

@app.route('/api/document/<int:id>')
def get_children(id):
    document = repo.get_document_by_id(id)
    parent_for = repo.get_child_documents(id)
    child_for = repo.get_parent_documents(id)
    result = {
        "document": document.__data__,
        "children": parent_for,
        "parents": child_for
    }
    return JsonTransformer().transform(result)


@app.route('/api/lem/<int:text_id>')
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


@app.route('/api/save_and_lem', methods=['POST'])
def save_and_lem():
    document_request = request.json
    doc = document_service.extract_doc_from_title(document_request["full_name"], document_request["text"], patterns)
    repo.save_doc(doc)
    lemmer = document_service.lem_text(document_request["text"])
    matched = document_service.find_links_in_lemed_text(lemmer, patterns)

    result = {
        "lemmed": lemmer.lemmed_string,
        "matched": matched
    }

    document_service.save_matched_links(matched, doc)
    return JsonTransformer().transform(result)


@app.route('/api/nodes')
def nodes_nice():
    documents = repo.get_all_documents()
    links = repo.get_all_links()
    imp_links = Mapper.map_impl_link_list_to_edges(implicit_links_service.get_implicit_links(50))
    print(imp_links)
    DAG = {
        "nodes": documents,
        "edges": links + imp_links
    }
    return JsonTransformer().transform(DAG)


@app.route('/api/save_file', methods=['POST'])
def get_documents():
    if 'file' not in request.files:
        print('No file part')
        return Response(status=401)
    file = request.files['file']
    ontology_service.extract_from_file(file)
    return Response(status=200)


@app.route("/api/ont_from_text", methods=['POST'])
def ont_from_text():
    document_request = request.json
    text = document_request["text"]
    file = StringIO(text)
    file.name = 'file.xml'
    result = ontology_service.extract_from_file(file)
    return Response(status=200)


@app.route("/api/tt", methods=['POST'])
def tt():
    file = request.files['file']
    result = ontology_service.extract_from_file(file)
    return JsonTransformer().transform(result)

@app.route("/api/imp")
def impl():
    result = implicit_links_service.get_implicit_links(50)
    return JsonTransformer().transform(result)

@app.route("/api/save_new_relation_indexes/<int:link_id>", methods=["POST"])
def save_new_relation_indexes(link_id):
    start_index = request.json["start_index"]
    end_index = request.json["end_index"]
    link = repo.get_link_by_id(link_id)
    link.start_index = start_index
    link.end_index = end_index
    repo.save_link(link)
    return Response(status=200)