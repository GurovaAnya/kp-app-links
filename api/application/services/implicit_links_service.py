import os

import requests

from ..repositories.relations_repository import RelationsRepository
from ..services.document_service import DocumentService
from ..models.implicit_link import ImplicitLink
from ..db.document import Document
from ..models.implicit_ref_document import ImplicitRefDocument

api = os.environ['IMPLICIT_LINKS_API']

class ImplicitLinksService:

    relations_repository = RelationsRepository()
    document_service = DocumentService()

    def __init__(self, patterns):
        self.patterns = patterns

    def map_names_to_db_entities(self, response) -> dict[str, Document]:
        names = response["names"]
        external_service_ids_to_local = {}
        for name in names:
            doc = self.document_service.extract_doc_requisites_from_title(name["name"], self.patterns)
            if doc is None:
                print("IMPLICIT_LINKS_SERVICE.map_names_to_db_entities. Пытались распарсить документ \"", name["name"], "\" но не получилось")
                continue
            print("IMPLICIT_LINKS_SERVICE.map_names_to_db_entities. Распарсили док: ", name, doc.date, doc.type, doc.number)
            existing_doc = self.relations_repository.find_document_by_number_date_type(doc.number, doc.date, doc.type)
            if existing_doc is not None:
                external_service_ids_to_local[name["id"]] = existing_doc.id
                print ("IMPLICIT_LINKS_SERVICE.map_names_to_db_entities. в нашей базе: ", existing_doc.id)

        return external_service_ids_to_local

    def get_implicit_links(self, threshold):
        links = self.get_links_from_outer_service()
        mapped_docs = self.map_names_to_db_entities(links)
        values = self.map_to_class(links["values"])
        values_that_matter = filter(lambda row: row.value >= threshold, values)
        result = []
        print(mapped_docs.keys())
        print(mapped_docs.values())
        for value in values_that_matter:
            print("IMPLICIT_LINKS_SERVICE.get_implicit_links. Value that matter: ", value.id_1, value.id_2, value.value)
            id_1 = value.id_1
            id_2 = value.id_2
            if id_1 in mapped_docs.keys() and id_2 in mapped_docs.keys():
                result.append(ImplicitLink(id_1=mapped_docs[id_1], id_2=mapped_docs[id_2], value=value.value))
        return result

    def get_implicit_links_for_id(self, id, threshold):
        all_links = self.get_implicit_links(threshold)
        for link in all_links:
            if link.id_1 == id:
                external_link = link.id_2
            elif link.id_2 == id:
                external_link = link.id_1
            else:
                continue

            doc = self.relations_repository.get_document_by_id(external_link)
            yield ImplicitRefDocument(
                id=external_link,
                name=doc.name,
                value=link.value
            )

    def get_links_from_outer_service(self):
        response = requests.get(api + "/api/SemanticSimilarity/GetSimilarityWithNames")
        print(response.json())
        return response.json()
        # return {
        #     "values": [
        #         {
        #             "id_1": "1",
        #             "id_2": "2",
        #             "value": 1
        #         },
        #         {
        #             "id_1": "1",
        #             "id_2": "3",
        #             "value": 0.5
        #         }
        #     ],
        #     "names": [
        #         {"id": "1",
        #          "name": 'Федеральный закон от 29 декабря 2012 N 273-ФЗ "Об образовании в Российской Федерации"'},
        #         {"id": "2", "name": 'Закон от 12 марта 2014 года N 308-ПК  "Об образовании в Пермском крае"'},
        #         {"id": "3", "name": 'Федеральный закон от 15 декабря 2014 N 555-ФЗ "О дипломе"'}
        #     ]
        # }

    def map_to_class(self, values):
        result = []
        for value in values:
            id_1 = value["firstDocumentId"]
            id_2 = value["secondDocumentId"]
            result.append(ImplicitLink(id_1=id_1, id_2=id_2, value=value["similarity"]))
        print("MAP_TO_CLASS: ", ([val.id_1 + " " + val.id_2 for val in result]))
        return result
