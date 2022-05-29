from ..utils.json_transformer import JsonTransformer
from ..services.ontology_extractor import OntologyExtractor
from ..services.links_analyser import LinksAnalyser


class OntologyService:
    ontology_extractor = OntologyExtractor()
    links_analyser = LinksAnalyser()

    def extract_from_file(self, file):
        result = self.ontology_extractor.extact_links_from_owl(file)
        docs = self.links_analyser.save_new_docs(result)
        links = self.links_analyser.map_links_to_docs(result, docs)
        self.links_analyser.save_links(links)
        return JsonTransformer().transform(links)
