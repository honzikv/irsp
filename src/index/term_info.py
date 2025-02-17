from typing import Dict

from src.index.document import Document
from src.index.document_info import DocumentInfo


class TermInfo:
    """
    Represents search_model information for specific term
    """

    def __init__(self, document: Document, term_name: str):
        """
        TermInfo can only be initialized with some document
        :param document: document that contains this term
        :param term_name: name of the term
        """
        # Documents are stored as a dictionary with document id as key and document as value
        doc_term_frequency = document.bow_log[term_name]
        self.documents: Dict[str, DocumentInfo] = {document.id: DocumentInfo(document, doc_term_frequency)}
        self.collection_frequency = doc_term_frequency
        self.document_frequency = 1

    def append_document(self, document: Document, term_name: str):
        """
        Appends document to the dictionary of documents
        :param document: document to be appended
        :param term_name: name of this term
        """

        # First we need to check whether a document
        # with the same id already exists in the dictionary
        if document.id in self.documents:
            # Remove the old document
            old_document_info = self.documents[document.id]
            self.document_frequency -= 1  # this is just to make the code cleaner without else statement
            del self.documents[document.id]

            # Recalculate collection frequency
            self.collection_frequency -= old_document_info.term_frequency

        # Append the new document
        term_frequency = document.bow_log[term_name]
        self.collection_frequency += term_frequency
        document_info = DocumentInfo(document, term_frequency)
        self.documents[document.id] = document_info
        self.document_frequency += 1

    def remove_document(self, document_id: str):
        """
        Removes document from the specified term
        :param document_id: id of the document
        :return:
        """
        if document_id not in self.documents:
            return  # nothing to do

        # Remove the document
        document_info = self.documents[document_id]
        self.collection_frequency -= document_info.term_frequency
        self.document_frequency -= 1
        del self.documents[document_id]

    def is_empty(self):
        """
        Checks whether this object has references to any documents
        :return: True if there are no references, False otherwise
        """
        return len(self.documents) == 0
