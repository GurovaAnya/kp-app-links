from flask import Flask, request
from flask_cors import CORS

from application.repositories.relations_repository import RelationsRepository
from application.services.document_service import DocumentService
from application.services.ontology_service import OntologyService
from application.utils.json_transformer import JsonTransformer
from application.services.implicit_links_service import ImplicitLinksService
from application.services.text_service import TextService
from application.controllers.deprecated_controller import deprecated_controller
from application.controllers.document_controller import document_controller
from application.controllers.extraction_controller import extraction_controller
from file_controller import file_controller
from application.controllers.link_controller import link_controller


app = Flask(__name__)
app.register_blueprint(deprecated_controller)
app.register_blueprint(document_controller)
app.register_blueprint(extraction_controller)
app.register_blueprint(file_controller)
app.register_blueprint(link_controller)


app.secret_key = "super secret key"
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

repo = RelationsRepository()
ontology_service = OntologyService()
document_service = DocumentService()
setting_file = open('application/settings/patters.txt', 'r')
patterns = setting_file.read().splitlines()
implicit_links_service = ImplicitLinksService(patterns)
text_service = TextService()

@app.route("/api/tt", methods=['POST'])
def tt():
    file = request.files['file']
    result = ontology_service.extract_from_file(file)
    return JsonTransformer().transform(result)

@app.route("/api/imp")
def impl():
    result = implicit_links_service.get_implicit_links(0.5)
    return JsonTransformer().transform(result)