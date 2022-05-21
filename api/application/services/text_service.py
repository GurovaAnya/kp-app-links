from ..repositories.relations_repository import RelationsRepository
import json

class TextService():
    texts = json.loads(open('application/services/text_mocks.json', 'r').read())

    repo = RelationsRepository()

    def get_text_from_service(self, ont_id: int):
        return next((obj for obj in self.texts if str(obj["id"]) == str(ont_id)), None)

    def get_text_by_id(self, id):
        print("id = ", id)
        text = self.repo.get_document_by_id(id)
        print("ont_id = ", text.ont_id)
        return self.get_text_from_service(text.ont_id)["text"]

    def get_all_texts_json(self):
        return json.dumps(self.texts)





