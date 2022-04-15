from typing import Dict

import numpy as np

from src.index.document import Document
from src.index.index import Index
from src.index.term_info import TermInfo
from src.preprocessing.preprocessing import Preprocessor
from src.search.cosine_similarity import cosine_similarity
from src.search.search_model import SearchModel


def calculate_tfidf(term_info: TermInfo, total_docs: int):
    """
    Calculates the tf-idf score for a given term
    :param term_info: TermInfo object
    :param total_docs: Total number of documents in the index
    :return: None
    """
    # inverse document frequency is constant for all documents
    idf = np.log10(total_docs / term_info.document_frequency)

    # Iterate over each document and calculate their tf-idf score
    for document_info in term_info.documents.values():
        tf = np.log10(1 + document_info.term_frequency)
        document_info.tfidf = tf * idf


def tfidf_vectorize_document(terms: Dict[str, TermInfo], document: Document) -> np.array:
    """
    Converts document to vector representation.
    :param terms:
    :param document:
    :return:
    """
    vector = np.zeros(len(terms))
    dim = 0
    for term, term_info in terms.items():
        if term in document.bow:
            vector[dim] = term_info.documents[document.doc_id].tfidf
        dim += 1

    return vector


def tfidf_vectorize_query(terms: Dict[str, TermInfo], query: Document, n_docs: int) -> np.array:
    """
    Converts query to vector representation.
    :param terms: Dictionary of terms and their information
    :param query: query as a Document instance
    :param n_docs: total number of documents in the index
    :return:
    """
    vector = np.zeros(len(terms.values()))
    dim = 0
    for term, term_info in terms.items():
        if term in query.bow:
            vector[dim] = np.log10(1 + query.bow[term]) * np.log10(n_docs / term_info.document_frequency)
        dim += 1

    return vector


class TfIdfModel(SearchModel):
    """
    TF-IDF model which uses cosine similarity for searching
    """

    def __init__(self, index: Index, preprocessor: Preprocessor):
        super().__init__(index)
        self.preprocessor = preprocessor

    def search(self, query: str, top_n: int = 10) -> list:
        """
        Search using tf-idf as a score
        :param query: query as a string
        :param top_n: number of results to return
        :return: list of tuples (score, document)
        """

        # Preprocess the query and get all terms
        tokens = self.preprocessor.get_tokens(query)
        terms = set(tokens)

        # Get all documents that contain at least one of the terms
        inverted_idx = self.inverted_idx

        # List of all unique documents that contain at least one of the terms
        documents = {}
        for term in terms:
            if term not in inverted_idx:
                continue

            for document_info in inverted_idx[term].documents.values():
                document = document_info.document
                if document not in documents:
                    documents[document.doc_id] = document

        # Get vector representation for query
        query_vector = tfidf_vectorize_query(inverted_idx, Document(-1, tokens, ''), len(documents))

        # Calculate the cosine similarity for each document
        results = []
        for doc_id, document in documents:
            doc_vec = tfidf_vectorize_document(inverted_idx, document)
            results.append((cosine_similarity(query_vector, doc_vec), document))

        return results
