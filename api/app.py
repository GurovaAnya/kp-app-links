from flask import Flask, request, flash, redirect, url_for, Response
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os

from application.services.document_service import DocumentService
from application.utils.json_transformer import JsonTransformer
from application.repositories.relations_repository import RelationsRepository
from application.services.ontology_extractor import OntologyExtractor
from application.services.links_analyser import LinksAnalyser

app = Flask(__name__)
app.secret_key = "super secret key"
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

repo = RelationsRepository()
ontology_extractor = OntologyExtractor()
links_analyser = LinksAnalyser()
document_service = DocumentService()
setting_file = open('settings/patters.txt', 'r')
patterns = setting_file.readlines()


@app.route('/api/document', methods=['POST'])
def add_document():
    document_request = request.json
    doc = document_service.extract_doc_from_title(document_request["full_name"], document_request["text"], patterns)
    doc = repo.save_doc(doc)
    return JsonTransformer().transform(doc)


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
    DAG = {
        "nodes": documents,
        "edges": links
    }
    return JsonTransformer().transform(DAG)


@app.route('/api/save_file', methods=['POST'])
def get_documents():
    document_request = request.json
    root = document_request["text"]
    filename = secure_filename(document_request["full_name"])
    path = os.path.join(os.environ['UPLOAD_FOLDER'], filename)
    myfile = open(path, "x")
    myfile.write(document_request["text"])
    return Response(status=200)
    # print(request.data)
    # if 'file' not in request.files:
    #     print('No file part')
    #     return Response(status=401)
    #     # return redirect(request.url)
    # file = request.files['file']
    # print(file)
    # if file.filename == '':
    #     print('No selected file')
    #     return Response(status=401)
    #     # return redirect(request.url)
    # # if file and allowed_file(file.filename):
    # filename = secure_filename(file.filename)
    # file.save(os.path.join(os.environ['UPLOAD_FOLDER'], filename))
    # return Response(status=200)
    #     #redirect(url_for('download_file', name=filename))


@app.route("/api/tt", methods=['POST'])
def tt():
    file = request.files['file']
    result = ontology_extractor.extact_links_from_owl(file)
    docs = links_analyser.save_new_docs(result)
    links = links_analyser.map_links_to_docs(result, docs)
    links_analyser.save_links(links)
    return JsonTransformer().transform(links)
