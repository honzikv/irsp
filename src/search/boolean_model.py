import logging
from typing import List, Set, Dict, Union, Tuple

from src.index.document import Document
from src.index.term_info import TermInfo
from src.preprocessing.boolean.boolean_parser import parse_boolean_query, QueryItem, BooleanOperator
from src.preprocessing.preprocessing import Preprocessor
from src.search.search_model import SearchModel

logger = logging.getLogger(__name__)


class BooleanModel(SearchModel):
    """
    Boolean Query Search model
    """

    def recalculate_terms(self, terms: List[TermInfo], n_docs: int):
        pass

    def __init__(self, index, preprocessor: Preprocessor):
        super().__init__(index)
        self.preprocessor = preprocessor
        self.documents = index.documents

    def search(self, query: str, n_items=None) -> Tuple[List[Document], Set[str]]:
        """
        Search for documents matching the query
        :param query: a boolean query
        :param n_items: number of items to return
        :return: List of all matching documents
        """
        try:
            detected_stopwords = set()
            preprocessed_query = self._preprocess_query(parse_boolean_query(query), detected_stopwords)
        except ValueError as e:
            logger.debug(str(e))
            raise ValueError('Query is not valid')

        if preprocessed_query is None:
            return [], detected_stopwords

        # DFS traverse the parsed query
        document_ids = self._dfs_traverse(preprocessed_query)
        return [self.documents[doc_id] for doc_id in document_ids], detected_stopwords

    def _preprocess_query(self, query: Union[QueryItem, str], detected_stopwords: Set[str] = None):
        if isinstance(query, str):
            # If we end up with query that is a string this means that there will be either one or more words
            tokens, stopwords = self.preprocessor.get_tokens(query, True)
            detected_stopwords.update(stopwords)
            if len(tokens) == 1:
                return tokens[0]
            if len(tokens) == 0:
                return None
            return QueryItem(items=tokens, operator=BooleanOperator.AND)

        # Now we must have either list of strings / query items
        preprocessed_items = []
        for item in query.items:
            preprocessed_item = self._preprocess_query(item, detected_stopwords)
            if isinstance(preprocessed_item, str):
                if preprocessed_item == '':
                    continue
            elif preprocessed_item is None or preprocessed_item.is_empty():
                continue
            preprocessed_items.append(preprocessed_item)

        query.items = preprocessed_items
        return query

    def _find_documents_matching_term(self, term) -> Set[str]:
        """
        Find all documents containing the term
        :param token: token to search
        :return:
        """
        return set(self.inverted_idx[term].documents.keys() if term in self.inverted_idx else [])

    def _dfs_traverse(self, query: Union[QueryItem, str]) -> Set[str]:
        """
        DFS traversal
        :param query: query item or a string
        :param detected_stopwords: set of all detected stopwords that gets updated if any new stopwords are found
        :return: List of ids of all matching documents
        """
        if isinstance(query, str):
            return self._find_documents_matching_term(query)

        items = query.items
        # Check whether the parameter is a string
        if isinstance(items, str):
            return self._find_documents_matching_term(items)

        # Else iterate over the list
        document_ids = set()
        for idx, item in enumerate(items):
            # Find matching documents for item
            matching_docs = self._find_documents_matching_term(item) if isinstance(item, str) else self._dfs_traverse(
                item)

            # If the operation is AND we need to intersect the sets
            if query.operator == BooleanOperator.AND:
                # If the index is 0 the set is empty so fill it with the docs for first item
                document_ids = matching_docs if idx == 0 else document_ids.intersection(matching_docs)
                continue

            # If the operation is OR we need to union the sets
            if query.operator == BooleanOperator.OR:
                document_ids = document_ids.union(matching_docs)
                continue

            # Otherwise we need a set that contains everything except the ids we have found for current item
            document_ids = set(self.documents.keys()).difference(matching_docs)

        return document_ids
