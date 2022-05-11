from abc import ABC, abstractmethod
from typing import List, Dict

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

    def recalculate(self, terms: List[TermInfo], n_docs: int):
        """
        Recalculates the model
        :param terms: new terms
        :param n_docs: new number of documents
        :return: None
        """
        return  # By default this does nothing since neither TF-IDF nor Boolean models need to recalculate
