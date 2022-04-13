# All indexes
from typing import Iterable

from src.index.document import Document
import numpy as np

indexes = {}

current_doc_id = 0


def get_next_doc_id():
    """
    Get next doc id for indexation
    :return: int
    """
    global current_doc_id
    doc_id = current_doc_id
    current_doc_id += 1
    return doc_id


class DocumentStats:
    """
    Represents stats for specific term in the document
    """

    def __init__(self, document: Document, occurrences: int):
        self.document = document  # Reference to the document
        self.tf = occurrences  # no. times the term appears in the document
        self._tfidf = None  # Term frequency inverse document frequency

    def set_tfidf(self, tfidf):
        self._tfidf = tfidf

    @property
    def tfidf(self):
        return self._tfidf

    def __str__(self):
        return f"""
        DocumentStats:
            document_id: {self.document.doc_id}
            term_count: {self.tf}
            term_frequency: {self.tf}
            tfidf: {self.tfidf}"""


class TermStats:
    """
    Represents stats for specific term in the corpus
    """

    def __init__(self, document: Document, term_str: str, occurrences: int):
        self.df = 1  # total number of terms in the corpus
        self.cf = occurrences  # total number of occurrences in the corpus
        self.text = term_str  # mostly for debugging, would not be used in production
        self.documents = {
            document.doc_id: DocumentStats(document, occurrences)
        }  # dictionary containing the documents where the term appears
        self._df = None  # Inverse document frequency

    def add_document_stats(self, document: Document, occurrences: int):
        """
        Updates the document stats for the term
        :param occurrences: number of times the term appears in the document
        :param document: the document
        :return:
        """
        self.cf += occurrences
        self.df += 1
        self.documents[document.doc_id] = DocumentStats(document, occurrences)

    def calculate_tf_idf(self, total_docs: int, log_tf=True):
        """
        Calculates tf-idf weights in each document
        :param: log_tf: if True, tf is calculated as log(1 + tf)
        :return:
        """
        for document in self.documents.values():
            tf = 1 + np.log10(
                document.tf) if log_tf and document.tf > 0 else document.tf  # term frequency as an integer
            idf = np.log10(total_docs / self.df)
            document.set_tfidf(tf * idf)

    def __str__(self):
        return f"""TermStats:
                collection_frequency: {self.cf}
                document_frequency: {self.df}
                documents: {''.join([str(doc) for doc in self.documents.values()])}"""


class Index:
    """
    Represents inverted index of all terms in the document
    """

    def __init__(self, name: str):
        self.name = name
        self.inverted_idx = {}  # term -> {doc_id -> DocumentStats}
        self.documents = []  # List of all documents

    def add_batch(self, batch: Iterable[Document]):
        """
        Inserts batch of documents to the index
        :param batch: Iterable of documents
        :return:
        """

        for document in batch:
            self.documents.append(document)
            bow = document.bow

            inverted_idx = self.inverted_idx
            for term, occurrences in bow.items():
                if term not in inverted_idx:
                    inverted_idx[term] = TermStats(document, term, occurrences)
                else:
                    inverted_idx[term].add_document_stats(document, occurrences)

        for term in inverted_idx:
            inverted_idx[term].calculate_tf_idf(len(self.documents))


def add_idx(idx: Index):
    if idx.name in indexes:
        raise ValueError(f"Index with name {idx.name} already exists")
    indexes[idx.name] = idx


def remove_idx(idx: Index):
    if idx.name not in indexes:
        raise ValueError(f"Index with name {idx.name} does not exist")
    del indexes[idx.name]


def get_idx(idx_name: str):
    if idx_name not in indexes:
        raise ValueError(f"Index with name {idx_name} does not exist")
    return indexes[idx_name]
