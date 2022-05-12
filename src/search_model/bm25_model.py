import logging
import math
from typing import Set, Dict

from src.index.document import Document
from src.preprocessing.preprocessing import Preprocessor
from src.search_model.search_model import SearchModel

logger = logging.getLogger(__name__)


class Bm25Model(SearchModel):

    def __init__(self, index, preprocessor: Preprocessor, k1: float = 1.2, b: float = 0.75):
        super().__init__(index)
        self.average_document_length = 0
        self.documents = index.documents
        self.preprocessor = preprocessor
        # since the model supports CRUD we cannot precompute the idf values but we can cache them until new
        # document is added
        self.idf_cache = {}
        self.n_docs = 0
        # Model params
        self.k1 = k1
        self.b = b

    def recalculate(self):
        self.idf_cache = {}
        self.average_document_length = sum([document.length for document in self.documents.values()]) / len(
            self.documents)
        self.n_docs = len(self.documents)

    def _calculate_document_bm25(self, document: Document, query: Dict[str, int]):
        score = 0.0
        for term, query_tf in query.items():
            if term not in document.bow_int:
                continue

            if term not in self.idf_cache:  # cache the term's idf value
                df = self.inverted_idx[term].document_frequency  # document frequency
                idf = math.log(1 + (self.n_docs - df + .5) / (df + .5))
                self.idf_cache[term] = idf
            else:
                idf = self.idf_cache[term]

            tf = document.bow_int[term]
            tf = (tf * (self.k1 + 1)) / (
                    tf + self.k1 * (1 - self.b + self.b * document.length / self.average_document_length))

            score += query_tf * tf * idf

        return score

    def search(self, query: str, top_n: int = None):
        """
        Search using bm25 as a score
        :param query: query as a string
        :param top_n: top n results to return
        :return: list of dictionaries where each contains the score and the document
        """
        tokens = self.preprocessor.get_tokens(query)
        _, query_terms = Document.calculate_bow(tokens)

        logger.debug(f"Searching for : {query_terms}")

        # Filter out all documents that contain at least one of the terms
        query_terms_keys = set(query_terms.keys())
        documents = self._get_documents_containing_terms(query_terms_keys)
        logger.info(f"Found {len(documents)} documents for terms {query_terms_keys}")

        # Calculate the score for each document
        results = [{} for _ in range(len(documents))]
        for i, document in enumerate(documents.values()):
            results[i]['score'] = self._calculate_document_bm25(document, query_terms)
            results[i]['document'] = document

        # Sort the documents by score
        results.sort(key=lambda x: x['score'], reverse=True)
        total_docs = len(results)

        # Return either the entire list if top_n is None, < 0 or greater than length of the array, otherwise return
        # a sublist
        return results if top_n is None or top_n <= 0 or top_n > len(results) else results[0:top_n], total_docs
