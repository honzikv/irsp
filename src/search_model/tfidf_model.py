import logging
from typing import Set, Dict, List

import numpy as np
import cProfile

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

    def _calculate_document_tfidf(self, document: Document, idf_cache: Dict[str, int], n_docs: int):
        """
        Calculates tfidf for given set of terms and appends all calculated idf values to passed idf cache
        :param terms:
        :param idf_cache:
        :return:
        """
        query_terms_tfidf: Dict[str, float] = {}
        query_norm = 0
        for term, tf in document.bow.items():
            if term in idf_cache:
                idf = idf_cache[term]
            else:
                idf = np.log(n_docs / self.inverted_idx[term].document_frequency)
                idf_cache[term] = idf
            term_tfidf = idf * tf  # tf * idf
            query_terms_tfidf[term] = term_tfidf  # set the tfidf value
            query_norm += term_tfidf * term_tfidf  # x(i-1)^2 + x(i)^2 + ...

        return query_terms_tfidf, query_norm

    def search(self, query: str, top_n: int = None):
        """
        Search using tf-idf as a score
        :param query: query as a string
        :param top_n: number of results to return
        :return: list of tuples (score, document)
        """

        # prof = cProfile.Profile()
        # prof.enable()

        # Preprocess the query and get all terms
        tokens = self.preprocessor.get_tokens(query)
        terms = set(tokens)

        logger.debug(f'Searching for {terms}')

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

        logger.info(f"Found {len(documents)} documents for terms {terms}")

        n_docs = len(self.inverted_idx)
        query = Document(doc_id='', tokens=tokens, text='', title='')
        idf_cache = {}  # So we do not calculate idf multiple times
        query_tfidf, query_norm = self._calculate_document_tfidf(query, idf_cache, n_docs)

        results: List[Dict] = [{} for _ in range(len(documents))]  # allocate array of dictionaries for results

        for idx, document in enumerate(documents.values()):
            document_tfidf, document_norm = self._calculate_document_tfidf(document, idf_cache, n_docs)
            similarity = 0
            for term, term_tfidf in query_tfidf.items():
                similarity += term_tfidf * document_tfidf[term] if term in document_tfidf else 0
            similarity /= (document_norm ** .5 * query_norm ** .5)
            results[idx]['score'] = similarity
            results[idx]['document'] = document
        # Sort the results by score descending
        results.sort(key=lambda x: x['score'], reverse=True)
        # prof.dump_stats('stats.prof')

        # Return either the entire list if top_n is None, < 0 or greater than length of the array, otherwise return
        # a sublist
        return results if top_n is None or top_n <= 0 or top_n > len(results) else results[0:top_n]
