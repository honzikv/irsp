# dictionary of all indices.py
from typing import Iterable, List, Dict

from src.api.indices import DocumentDto
from src.index.document import Document
from src.index.term_info import TermInfo
from src.preprocessing.preprocessing import Preprocessor
from src.search.search_model import SearchModel
from src.search.tfidf_model import calculate_tfidf

# All indexes
_indices = {}

# Default search
default_models = ['tf_idf', 'boolean']

# Additional search that can be added to the default search
additional_models = ['transformers', 'doc2vec']


class IndexConfig:
    """
    Configuration for the index object
    """

    def __init__(self, name, models, preprocessor: Preprocessor):
        """
        Constructor for the IndexConfig object
        :param name: name of the index
        :param models: list of search models to use
        :param preprocessor: preprocessor to use
        """
        for model in models:
            if model not in additional_models:
                raise ValueError(f'{model} is not a valid model')

        self.name = name
        self.models = models + default_models
        self.preprocessor = preprocessor


class Index:
    """
    Index is a structure that holds all specific documents of the same type (semantically)
    """

    def __init__(self, config: IndexConfig, initial_batch: List[Document]):
        self.config: IndexConfig = config
        self.inverted_idx: Dict[str, TermInfo] = {}  # inverted index for searching
        self.documents: Dict[int, Document] = {}  # dictionary of all documents in the index
        self._create_initial_batch(initial_batch)
        self.models: Dict[str, SearchModel] = {}
        self.next_doc_id = 0  # next document id to be used

    def get_next_doc_id(self):
        current_id = self.next_doc_id
        self.next_doc_id += 1
        return current_id

    def _recalculate_terms(self, terms):
        n_docs = len(self.documents)
        # Recalculate all terms that were changed
        for term in terms:
            calculate_tfidf(term, n_docs)

    def add_batch(self, batch: List[Document]):
        """
        Adds batch of documents to the index, if some documents already exist they will be replaced
        :param batch: Iterable of documents
        :return: None
        """

        # Create a set of all terms to recalculate so we do not recalculate the same term multiple times
        terms_to_recalculate = set()
        for document in batch:
            doc_terms = set(document.tokens)
            for term in doc_terms:
                if term not in self.inverted_idx:
                    self.inverted_idx[term] = TermInfo(document, term)
                else:
                    self.inverted_idx[term].append_document(document, term)
                    terms_to_recalculate.add(self.inverted_idx[term])

            # Add document to the index
            self.documents[document.doc_id] = document

        # Recalculate all terms that were changed
        self._recalculate_terms(terms_to_recalculate)

    def add_document(self, document: Document):
        """
        Adds a single document to the index
        :param document: Document to be added
        :return: None
        """
        self.add_batch([document])

    def preprocess_document(self, document: DocumentDto):
        """
        Preprocesses DocumentDto object
        :param document: DocumentDto object
        :return: preprocessed Document object
        """
        document_id = document.docId if document.docId else self.get_next_doc_id()
        document_tokens = self.config.preprocessor.get_tokens(document.text)
        return Document(document_id, document_tokens, document.text, document.additionalProperties)

    def preprocess_batch(self, documents: List[DocumentDto]):
        """
        Preprocesses batch of documents
        :param documents: List of DocumentDto objects
        :return: List of preprocessed Document objects
        """
        return [self.preprocess_document(document) for document in documents]

    def delete_batch(self, batch: List[int]):
        """
        Deletes documents from the index
        :param batch: list of document indices.py to delete
        :return: None
        """

        # Same approach as in add_batch - keep unique terms to update later
        terms_to_recalculate = set()
        for doc_id in batch:
            if doc_id not in self.documents:
                continue  # nothing to delete

            document = self.documents[doc_id]
            doc_terms = set(document.tokens)
            for term in doc_terms:
                terms_to_recalculate.add(term)
                term_info = self.inverted_idx[term]
                term_info.remove_document(document.doc_id)

            # Delete the document
            del self.documents[doc_id]

        # Recalculate all terms that were changed
        self._recalculate_terms(terms_to_recalculate)

    def delete_document(self, doc_id: int):
        """
        Deletes a single document from the index
        :param doc_id: Document to delete
        :return: None
        """
        self.delete_batch([doc_id])

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

    def search(self, query: str, models: List[str], n_items: int = 10) -> dict:
        """
        Performs search on all models
        :param query: sought query
        :param models:
        :param n_items: number of items to return
        :return: dictionary for json response
        """

        res = {}  # dictionary for response
        for model_name in models:
            if model_name not in self.models:
                raise ValueError(f'{model_name} does not exist in index {self.config.name}')

            model = self.models[model_name]
            documents = model.search(query, n_items)
            res[model_name] = {
                'documents': documents,
                'count': len(documents)
            }

        return res


def get_index(name: str) -> Index:
    """
    Gets index by name
    :param name: Name of the index
    :return: Index
    """
    if name not in _indices:
        raise ValueError(f'Index {name} does not exist')
    return _indices[name]


def add_index(name: str, index: Index):
    """
    Adds index to the list of indices.py
    :param name: Name of the index
    :param index: Index to add
    :return: None
    """
    if name in _indices:
        raise ValueError(f'Index {name} already exists')
    _indices[name] = index


def delete_index(name: str):
    """
    Deletes index from the list of indices
    :param name: Name of the index
    :return: None
    """
    if name not in _indices:
        raise ValueError(f'Index {name} does not exist')
    del _indices[name]
