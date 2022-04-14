import numpy as np

from src.index.term_info import TermInfo


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
