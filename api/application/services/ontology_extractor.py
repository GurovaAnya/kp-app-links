from rdflib import ConjunctiveGraph
from .extracted_document import ExtractedDocument
from .extracted_link import ExtractedLink
from .extraction_result import ExtractionResult


class OntologyExtractor:

    def extact_links_from_owl(self, file):
        g = ConjunctiveGraph(identifier="owl")
        g.parse(file, format="application/rdf+xml")
        knows_query = """
        select ?parentDoc ?parentDocName ?parentDate ?parentType ?parentNumber ?childDoc ?childDocName ?childDate ?childType ?childNumber
        where {
        ?parentDocRequisite <http://webprotege.stanford.edu/R7Uu5DolqliNn7j7tLoJ4vj> ?parentDoc .
        ?parentDoc <http://webprotege.stanford.edu/Rm6lpfWfl1n8iyEPmIwHsq> ?childDoc .
        optional {?childDocRequisite <http://webprotege.stanford.edu/R7Uu5DolqliNn7j7tLoJ4vj> ?childDoc .}
        optional {?parentDoc rdfs:label ?parentDocName}
        optional {?parentDocRequisite <http://webprotege.stanford.edu/RBPvDB8ifRxnRSxe1qOHCvh> ?parentDate}
        optional {?parentDocRequisite <http://webprotege.stanford.edu/R9VvMsvB05wdBTf4FXqOGKX> ?parentType}
        optional {?childDoc rdfs:label ?childDocName}
        optional {?childDocRequisite <http://webprotege.stanford.edu/RBPvDB8ifRxnRSxe1qOHCvh> ?childDate}
        optional {?childDocRequisite <http://webprotege.stanford.edu/R9VvMsvB05wdBTf4FXqOGKX> ?childType}
        optional {?parentDocRequisite <http://webprotege.stanford.edu/R7iHQXGPKEYCqns6dD7DXoY> ?parentNumber}
        optional {?childDocRequisite <http://webprotege.stanford.edu/R7iHQXGPKEYCqns6dD7DXoY> ?childNumber}
        }"""

        qres = g.query(knows_query)
        documents = {}
        links = []
        for row in qres:
            print(row)
            child = ExtractedDocument(
                ontology_id=str(row["childDoc"]),
                name=str(row["childDocName"]),
                type=str(row["childType"]),
                date=str(row["childDate"]),
                number=str(row["childNumber"])
            )

            if child.ontology_id not in documents:
                documents[child.ontology_id] = child

            parent = ExtractedDocument(
                ontology_id=str(row["parentDoc"]),
                name=str(row["parentDocName"]),
                type=str(row["parentType"]),
                date=str(row["parentDate"]),
                number=str(row["parentNumber"])
            )

            if parent.ontology_id not in documents:
                documents[parent.ontology_id] = parent

            link = ExtractedLink(
                child=child.ontology_id,
                parent=parent.ontology_id
            )

            links.append(link)

        return ExtractionResult(documents, links)
