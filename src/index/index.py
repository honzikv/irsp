# dictionary of all indices
from typing import Iterable, List, Dict

from src.index.document import Document

# All indexes
from src.index.term_info import TermInfo
from src.search.tfidf import calculate_tfidf

_indices = {}

# Default search
default_models = ['tf_idf', 'boolean']

# Additional search that can be added to the default search
additional_models = ['transformers', 'doc2vec']


class IndexConfig:
    """
    Configuration for the index object
    """

    def __init__(self, name, models):
        for model in models:
            if model not in additional_models:
                raise ValueError(f'{model} is not a valid model')

        self.name = name
        self.models = models + default_models


class Index:
    """
    Index is a structure that holds all specific documents of the same type (semantically)
    """

    def __init__(self, config: IndexConfig, initial_batch: List[Document]):
        self.config: IndexConfig = config
        self.inverted_idx: Dict[str, TermInfo] = {}  # inverted index for searching
        self.documents: Dict[int, Document] = {}  # dictionary of all documents in the index
        self._create_initial_batch(initial_batch)

    def add_batch(self, documents: Iterable[Document]):
        """
        Adds batch of documents to the index, if some documents already exist they will be replaced
        :param documents: Iterable of documents
        :return: None
        """
        pass

    def _create_initial_batch(self, documents: List[Document]):
        """
        Creates initial batch of documents
        :param documents:
        :return:
        """
        if len(documents) == 0:
            return

        for document in documents:
            self.documents[document.doc_id] = document

            # Get bag of words of the document - this will be used to assign documents to terms
            bow = document.bow

            inverted_idx = self.inverted_idx
            for term, occurrences in bow.items():
                if term not in inverted_idx:
                    inverted_idx[term] = TermInfo(document, term)
                else:
                    inverted_idx[term].append_document(document, term)

        n_docs = len(self.documents.values())
        # Now calculate the tf_idf for all terms
        for term_info in self.inverted_idx.values():
            calculate_tfidf(term_info, n_docs)

