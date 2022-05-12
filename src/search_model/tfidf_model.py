import logging
import math
from typing import Dict, List

from src.index.document import Document
from src.preprocessing.preprocessing import Preprocessor
from src.search_model.search_model import SearchModel

logger = logging.getLogger(__name__)


class TfIdfModel(SearchModel):
    """
    TF-IDF model which uses cosine similarity for searching.
    """

    def __init__(self, index, preprocessor: Preprocessor):
        super().__init__(index)
        self.preprocessor = preprocessor
        self.documents = index.documents
        # since the model supports CRUD we cannot precompute the idf values but we can cache them until new
        # document is added
        self.idf_cache = {}
        self.n_docs = 0

    def _calculate_document_tfidf(self, document: Document):
        """
        Calculates tfidf for given set of terms and appends all calculated idf values to passed idf cache
        :param document: document to calculate tfidf for
        :return:
        """
        terms_tfidf: Dict[str, float] = {}
        norm = 0.0
        for term, tf in document.bow_log.items():
            if term not in self.inverted_idx:  # ignore any term that is not in inverted index
                continue

            if term in self.idf_cache:
                idf = self.idf_cache[term]
            else:
                idf = math.log(self.n_docs / self.inverted_idx[term].document_frequency)
                self.idf_cache[term] = idf
            term_tfidf = idf * tf  # tf * idf
            terms_tfidf[term] = term_tfidf  # set the tfidf value
            norm += term_tfidf * term_tfidf  # x(i-1)^2 + x(i)^2 + ...

        return terms_tfidf, norm

    def search(self, query: str, top_n: int = None):
        """
        Search using tf-idf as a score
        :param query: query as a string
        :param top_n: number of results to return
        :return: list of tuples (score, document) and total number of documents
        """
        # Preprocess the query and get all terms
        tokens = self.preprocessor.get_tokens(query)
        terms = set(tokens)

        logger.debug(f'Searching for {terms}')

        # Get all documents that contain at least one of the terms
        documents = self._get_documents_containing_terms(terms)

        logger.info(f"Found {len(documents)} documents for terms {terms}")
        query = Document(doc_id='', tokens=tokens, text='', title='')
        query_tfidf, query_norm = self._calculate_document_tfidf(query)

        results: List[Dict] = [{} for _ in range(len(documents))]  # allocate array of dictionaries for results

        for idx, document in enumerate(documents.values()):
            document_tfidf, document_norm = self._calculate_document_tfidf(document)
            similarity = 0.0
            for term, term_tfidf in query_tfidf.items():
                similarity += term_tfidf * document_tfidf[term] if term in document_tfidf else 0.0
            similarity /= (document_norm ** .5 * query_norm ** .5)
            results[idx]['score'] = similarity
            results[idx]['document'] = document
        # Sort the results by score descending

        total_docs = len(results)
        results.sort(key=lambda x: x['score'], reverse=True)

        # Return either the entire list if top_n is None, < 0 or greater than length of the array, otherwise return
        # a sublist
        return results if top_n is None or top_n <= 0 or top_n > len(results) else results[0:top_n], total_docs

    def recalculate(self):
        """
        This model does not recalculate anything but we want to invalide the idf cache
        :return: None
        """
        self.idf_cache = {}
        self.n_docs = len(self.documents)
