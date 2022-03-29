from flask import Flask
from flask import request

from application.services.document_service import DocumentService
from application.utils.json_transformer import JsonTransformer
from application.repositories.relations_repository import RelationsRepository


app = Flask(__name__)

repo = RelationsRepository()
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
    documents = get_all_documents()
    links = get_all_links()
    DAG = {
        "nodes": documents,
        "edges": links
    }
    return JsonTransformer().transform(DAG)


def get_all_documents():
    return [
        {
            'data':
                {
                    "id": 1,
                    'name': "Постановление Правительства российской федерации от 31 декабря 2021 г. № 2611"
                }
        },
        {
            'data':
                {
                    'id': 2,
                    'name': 'Постановление Правительства РФ от 10 февраля 2021 г. N 147'
                }
        },
        {
            'data':
                {
                    'id': 3,
                    'name': 'Постановление Правительства РФ от 10 марта 2020 г. N 263'
                }
        },
        {
            'data':
                {
                    'id': 4,
                    'name': 'Статья 214 ГК РФ'
                }
        },
        {
            'data':
                {
                    'id': 5,
                    'name': 'Статья 215 ГК РФ'
                }
        },
        {
            'data':
                {
                    'id': 6,
                    'name': 'Статья 9 ТК РФ'
                }
        },
        {
            'data':
                {
                    'id': 7,
                    'name': 'Статья 125 ГК РФ'
                }
        }
    ]

def get_all_links():
    return [
        {
            'data':
                {
                    "source": 1,
                    "target": 2
                }
        },
        {
            'data':
                {
                    "source": 2,
                    "target": 3
                }
        },
        {
            'data':
                {
                    "source": 4,
                    "target": 7
                }
        }
    ]