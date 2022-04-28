from typing import List, Set, Dict

from src.index.document import Document
from src.index.term_info import TermInfo
from src.preprocessing.boolean.boolean_parser import parse_boolean_query, QueryItem, BooleanOperator
from src.preprocessing.preprocessing import Preprocessor
from src.search.search_model import SearchModel


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

    def search(self, query: str, n_items=None) -> List[Document]:
        """
        Search for documents matching the query
        :param query: a boolean query
        :param n_items: number of items to return
        :return: List of all matching documents
        """
        try:
            parsed_query = parse_boolean_query(query)
        except ValueError:
            raise ValueError('Query is not valid')

        # DFS traverse the parsed query
        document_ids = self._dfs_traverse(parsed_query)
        return [self.documents[doc_id] for doc_id in document_ids]

    def _find_documents_for_token(self, token: str) -> Set[int]:
        """
        Find all documents containing the token
        :param token: token to search
        :return: List of ids of all matching documents
        """
        # Preprocess the token into term(s)
        terms = self.preprocessor.get_tokens(token)

        # Iterate over "each" term - there should really be only one but we need to treat this as a list
        docs = set()
        for term in terms:
            # Get the term info
            if term not in self.inverted_idx:
                continue  # if there is none simply continue
            term_info = self.inverted_idx[term]
            docs.update([x.document.doc_id for x in term_info.documents.values()])

        return docs

    def _dfs_traverse(self, query: QueryItem) -> Set[int]:
        """
        AND search
        :param items: list of QueryItems
        :return: List of ids of all matching documents
        """

        items = query.items
        # Check whether the parameter is a string
        if isinstance(items, str):
            return self._find_documents_for_token(items)

        # Else iterate over the list
        docs = set()
        for idx, item in enumerate(items):
            # Find matching documents for item
            matching_docs = self._find_documents_for_token(item) if isinstance(item, str) else self._dfs_traverse(item)

            # If the operation is AND we need to intersect the sets
            if query.operator == BooleanOperator.AND:
                # If the index is 0 the set is empty so fill it with the docs for first item
                docs = matching_docs if idx == 0 else docs.intersection(matching_docs)
                continue

            # If the operation is OR we need to union the sets
            if query.operator == BooleanOperator.OR:
                docs = docs.union(matching_docs)
                continue

            # Otherwise we need a set that contains everything except the ids we have found for current item
            docs = set(self.documents.keys()).difference(matching_docs)

        return docs
