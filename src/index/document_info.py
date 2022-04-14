from src.index.document import Document


class DocumentInfo:
    """
    Represents information about document to specific term
    """

    def __init__(self, document: Document, frequency: int):
        """
        Initializes new instance of DocumentInfo
        :param document: reference to the document
        :param frequency: frequency of the term in the document, this value is always integer
        """
        self.document = document
        self.term_frequency = frequency
        self.tfidf = None
        # TODO more fields for specific models

    def __str__(self):
        return f"""
                DocumentStats:
                    document_id: {self.document.doc_id}
                    # term occurrences: {self.term_frequency}
                    tfidf: {self.tfidf}"""

