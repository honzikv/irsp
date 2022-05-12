from abc import ABC, abstractmethod
from typing import List, Dict, Set

from src.index.term_info import TermInfo


class SearchModel(ABC):
    """
    Interface for search_model models
    """

    @abstractmethod
    def __init__(self, index):
        """
        Constructor
        :param index: index to search_model in
        """
        self.inverted_idx: Dict[str, TermInfo] = index.inverted_idx

    @abstractmethod
    def search(self, query: str, n_items=None):
        """
        Search for documents matching the query
        :param query: sought query
        :param n_items: number of items to return
        :return: list of all documents matching the query
        """
        pass

    def recalculate(self):
        """
        Recalculates the model
        :return: None
        """
        return  # By default this does nothing since neither TF-IDF nor Boolean models need to recalculate

    def _get_documents_containing_terms(self, terms: Set[str]):
        """
        Returns all documents containing at least one of the given terms
        :param terms:
        :return:
        """
        # List of all unique documents that contain at least one of the terms
        documents = {}
        for term in terms:
            if term not in self.inverted_idx:  # ignore any term that is not in inverted index
                continue

            # now iterate for each document that has at least one of the term and add it to the list
            for document_info in self.inverted_idx[term].documents.values():
                document = document_info.document
                if document.id not in documents:
                    documents[document.id] = document

        return documents
