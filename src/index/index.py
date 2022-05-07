# dictionary of all indices.py
import json
import uuid
from datetime import datetime
from typing import List, Dict

from fastapi import UploadFile

from src.api.indices_dtos import DocumentDto, IndexDto, ModelVariant, QueryDto
from src.index.document import Document
from src.index.index_config import IndexConfig
from src.index.term_info import TermInfo
from src.search.boolean_model import BooleanModel
from src.search.search_model import SearchModel
from src.search.tfidf_model import calculate_tfidf, TfIdfModel

# All indexes
_indices = {}
models = ['tf_idf', 'bool', 'transformers']


class Index:
    """
    Index is a structure that holds all specific documents of the same type (semantically)
    """

    def __init__(self, config: IndexConfig, initial_batch: List[Document]):
        self.config: IndexConfig = config
        self.inverted_idx: Dict[str, TermInfo] = {}  # inverted index for searching
        self.documents: Dict[uuid.UUID, Document] = {}  # dictionary of all documents in the index
        self._create_initial_batch(initial_batch)
        self.models: Dict[str, SearchModel] = {
            'tfidf': TfIdfModel(self, self.config.preprocessor),
            'bool': BooleanModel(self, self.config.preprocessor)
        }

    def get_next_doc_id(self):
        """
        Returns next document id to be used
        :return: uuid.UUID
        """
        return uuid.uuid4()

    def _recalculate_terms(self, terms):
        """
        Recalculates passed terms in the index
        :param terms: Iterable of TermInfo objects
        :return: None
        """
        n_docs = len(self.documents)
        for model in self.models.values():
            model.recalculate_terms(terms, n_docs)

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

            # if there is already document with the same id remove it
            if document.doc_id in self.documents:
                self.delete_document(document.doc_id)

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
        Preprocesses DocumentDto object. If the document does not have any id it will be assigned a new one
        :param document: DocumentDto object
        :return: preprocessed Document object
        """
        document_id = document.docId if document.docId else self.get_next_doc_id()
        document_tokens = self.config.preprocessor.get_tokens(document.text)
        return Document(document_id, document_tokens, document.text, datetime.now(), document.additionalProperties)

    def preprocess_batch(self, documents: List[DocumentDto]):
        """
        Preprocesses batch of documents
        :param documents: List of DocumentDto objects
        :return: List of preprocessed Document objects
        """
        return [self.preprocess_document(document) for document in documents]

    def delete_batch(self, batch: List[uuid.UUID]):
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

        self._recalculate_terms(terms_to_recalculate)

    def delete_document(self, doc_id: uuid.UUID):
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

    def search(self, query_dto: QueryDto) -> list:
        """
        Performs search on all models
        :param query_dto: QueryDto object
        :return: dictionary for json response
        """
        query, model, n_items = query_dto.query, query_dto.model, query_dto.topK
        # Model variant gets validated in the controller via Pydantic, so we can assume it's valid
        search_model = self.models[model.value]

        search_result = search_model.search(query, n_items)

        if model == ModelVariant.BOOL:
            # For boolean model return score as NaN
            return [{'score': None, 'document': DocumentDto.from_domain_object(item)} for item in search_result]

        # Else return score and document
        return [{'score': item['score'], 'document': DocumentDto.from_domain_object(item['document'])} for item in
                search_result]

    def to_dto(self, n_example_docs=10) -> IndexDto:
        """
        Converts this to IndexDto
        :return: instance of IndexDto
        """
        n_example_docs = n_example_docs if len(self.documents) > n_example_docs else len(self.documents)
        example_docs = [DocumentDto.from_domain_object(doc) for doc in list(self.documents.values())[:n_example_docs]]
        return IndexDto(
            name=self.config.name,
            models=list(self.models.keys()),
            nTerms=len(self.inverted_idx),
            nDocs=len(self.documents),
            exampleDocuments=example_docs
        )

    def _parse_document_from_dict(self, doc_dict: dict) -> Document:
        if 'text' not in doc_dict:
            raise ValueError('Document text cannot be empty')

        # Map to DocumentDto and let the index preprocess the text
        return self.preprocess_document(
            DocumentDto(docId=doc_dict['docId'] if 'docId' in doc_dict else None, text=doc_dict['text'],
                        additionalProperties={prop: val for prop, val in doc_dict.items() if prop != 'text'}))

    def add_json_to_index(self, upload_file: UploadFile) -> List[Document]:
        """
        Adds json to index if possible. Throws ValueError if json is not valid
        :param upload_file:
        :return: List of all processed documents
        """
        try:
            json_data = json.load(upload_file.file)
            if isinstance(json_data, dict):
                # If its dict we have a single document
                doc = self._parse_document_from_dict(json_data)
                self.add_document(doc)
                return [doc]
            elif isinstance(json_data, list):
                # Else we have an array of documents
                docs = [self._parse_document_from_dict(doc) for doc in json_data]
                self.add_batch(docs)
                return docs
            else:
                # Or something random so throw an error
                raise ValueError()
        except ValueError as e:
            raise ValueError(
                'Invalid JSON file received. Make sure the file is a valid JSON '
                'array / object containing only Document(s).'
            )


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


def get_all_indices() -> List[IndexDto]:
    """
    Gets all indices
    :return: List of indices
    """
    return list(map(lambda x: x.to_dto(), _indices.values()))
