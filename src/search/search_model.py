from abc import ABC, abstractmethod


class SearchModel(ABC):
    """
    Interface for search models
    """

    @abstractmethod
    def __init__(self, index):
        """
        Constructor
        :param index: index to search in
        """
        self.inverted_idx = index.inverted_idx

    @abstractmethod
    def search(self, query: str, n_items=None):
        """
        Search for documents matching the query
        :param query: sought query
        :param n_items: number of items to return
        :return: list of all documents matching the query
        """
        pass
