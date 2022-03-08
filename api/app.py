import time
from flask import Flask
from flask import request
from application.services.lemmer import Lemmer
from application.utils.json_transformer import JsonTransformer


app = Flask(__name__)

@app.route('/lem')
def lem():
    text = request.args["text"]
    lemmer = Lemmer(text)
    lemmed = lemmer.get_lemmed_string()
    setting_file = open('settings/patters.txt', 'r')
    patterns = setting_file.readlines();
    matched = list(lemmer.find_words(patterns))

    result = {
        "lemmed": lemmed,
        "matched": matched
    }

    return JsonTransformer().transform(result)


@app.route('/map')
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
