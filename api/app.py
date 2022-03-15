from flask import Flask
from flask import request
from application.services.lemmer import Lemmer
from application.utils.json_transformer import JsonTransformer
from application.repositories.relations_repository import RelationsRepository
from application.db.BaseModel import Link, Document
from flask import Response


app = Flask(__name__)


@app.route('api/document', methods=['POST'])
def add_document():
    repo = RelationsRepository()
    document_request = request.json
    lemmer = Lemmer(document_request["full_name"])
    lemmed = lemmer.get_lemmed_string()
    print(lemmer.text)
    setting_file = open('settings/patters.txt', 'r')
    patterns = setting_file.readlines()
    matched = list(lemmer.find_words(patterns))
    print(matched)
    first_match = matched[0]
    doc = Document(name=document_request["full_name"],
                   number=first_match.number,
                   date=first_match.date,
                   authority=first_match.authority,
                   type=first_match.type,
                   text=document_request["text"]
                   )

    repo.save_doc(doc)

    return Response(status=201)


@app.route('api/lem/<int:text_id>')
def lem(text_id):
    repo = RelationsRepository()
    text = repo.get_document_by_id(text_id).text
    print(text)
    lemmer = Lemmer(text)
    lemmed = lemmer.get_lemmed_string()
    setting_file = open('settings/patters.txt', 'r')
    patterns = setting_file.readlines()
    matched = list(lemmer.find_words(patterns))

    result = {
        "lemmed": lemmed,
        "matched": matched
    }

    for link in matched:
        child_doc = repo.find_document_by_params(doc_type=link.type, authority=link.authority, number=link.number, date=link.date)
        db_link = Link(parent_id=text_id, child_id=child_doc.id, start_index=link.start_index, end_index=link.end_index)
        repo.save_link(db_link)

    return JsonTransformer().transform(result)


@app.route('api/map')
def map():
    DAG = {
        'nodes': [
            {'data': {"id": "j", 'name': "Закон 1"}},
            {'data': {"id": "e", 'name': "Закон 2"}},
            {'data': {"id": "k", 'name': "Закон 3"}},
            {'data': {"id": "g", 'name': "Закон 4"}}
        ],
        'edges': [
            {'data': {'source': "j", 'target': "e"}},
            {'data': {'source': "j", 'target': "k"}},
            {'data': {'source': "j", 'target': "g"}},
            {'data': {'source': "e", 'target': "j"}}
        ]
    }
    return JsonTransformer().transform(DAG)


@app.route('api/test')
def test():
    repo = RelationsRepository()
    documents = repo.get_all_documents()
    links = repo.get_all_links()
    DAG = {
        "nodes": documents,
        "edges": links
    }
    return JsonTransformer().transform(DAG)
