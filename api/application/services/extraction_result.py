from .extracted_link import ExtractedLink
from .extracted_document import ExtractedDocument

class ExtractionResult:

    def __init__(self, documents: dict[str, ExtractedDocument], links: list[ExtractedLink]):
        self.documents = documents
        self.links = links
