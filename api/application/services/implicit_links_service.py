from ..repositories.relations_repository import RelationsRepository
from ..services.document_service import DocumentService
from ..models.implicit_link import ImplicitLink
from ..db.document import Document


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
            existing_doc = self.relations_repository.find_document_by_number_date_type(doc.number, doc.date, doc.type)
            if existing_doc is not None:
                external_service_ids_to_local[name["id"]] = existing_doc.id
            print("----------")
            print(name, doc.date, doc.type, doc.number)
            print("--------------")

        return external_service_ids_to_local

    def get_implicit_links(self, threshold):
        links = self.get_links_from_outer_service()
        mapped_docs = self.map_names_to_db_entities(links)
        values = self.map_to_class(links["values"])
        values_that_matter = filter(lambda row: row.value >= threshold, values)
        result = []
        print(mapped_docs.keys())
        for value in values_that_matter:
            id_1 = value.id_1
            id_2 = value.id_2
            if id_1 in mapped_docs.keys() and id_2 in mapped_docs.keys():
                result.append(ImplicitLink(id_1=mapped_docs[id_1], id_2=mapped_docs[id_2], value=value.value))
        return result

    def get_links_from_outer_service(self):
        return {
            "values": [
                {
                    "id_1": "1",
                    "id_2": "2",
                    "value": 100
                },
                {
                    "id_1": "1",
                    "id_2": "3",
                    "value": 50
                }
            ],
            "names": [
                {"id": "1",
                 "name": 'Федеральный закон от 29 декабря 2012 N 273-ФЗ "Об образовании в Российской Федерации"'},
                {"id": "2", "name": "Конституция РФ"},
                # {"id": "2", "name": 'Федеральный закон от 15 декабря 2015 N 545-ФЗ "О чем-то еще"'},
                {"id": "3", "name": 'Федеральный закон от 15 декабря 2014 N 555-ФЗ "О дипломе"'}
            ]
        }

    def map_to_class(self, values):
        result = []
        for value in values:
            print("@@@@@@")
            print(value)
            id_1: str = str(value["id_1"][0])
            id_2: str = str(value["id_2"][0])
            print(id_1)
            result.append(ImplicitLink(id_1=id_1, id_2=id_2, value=value["value"]))
        return result
