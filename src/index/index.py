import json
import logging
import uuid
from datetime import datetime
from typing import List, Dict

from fastapi import UploadFile

from src.api.dtos import DocumentDto, IndexDto, ModelVariant, QueryDto, DocumentSearchResultDto
from src.index.document import Document
from src.index.index_config import IndexConfig
from src.index.term_info import TermInfo
from src.search_model.bm25_model import Bm25Model
from src.search_model.boolean_model import BooleanModel
from src.search_model.search_model import SearchModel
from src.search_model.tfidf_model import TfIdfModel

# All indexes
_indices = {}
models = ['tf_idf', 'bool', 'bm25']

logger = logging.getLogger(__name__)


class Index:
    """
    Index is a structure that holds all specific documents of the same type (semantically)
    """

    def __init__(self, config: IndexConfig, initial_batch: List[Document] = None):
        self.config: IndexConfig = config
        self.inverted_idx: Dict[str, TermInfo] = {}  # inverted index for searching
        self.documents: Dict[str, Document] = {}  # dictionary of all documents in the index
        self.models: Dict[str, SearchModel] = {
            'tfidf': TfIdfModel(self, self.config.preprocessor),
            'bool': BooleanModel(self, self.config.preprocessor),
            'bm25': Bm25Model(self, self.config.preprocessor)
        }

        if initial_batch:  # add initial batch if it is provided
            self.add_batch(initial_batch)

    @staticmethod
    def get_next_doc_id() -> str:
        """
        Returns next document id to be used
        :return: str
        """
        return str(uuid.uuid4())

    def _recalculate_models(self):
        """
        Runs recalculate() method of all models
        :return:
        """
        for model in self.models.values():
            model.recalculate()

    def add_batch(self, documents: List[Document]):
        """
        Adds batch of documents to the index, if some documents already exist they will be replaced
        :param documents: list of documents to be added
        :return:
        """
        # Iterate over the list
        for document in documents:
            # If the document already exists in the index, remove it
            if document.id in self.documents:
                self.delete_document(document.id)

            # Get list of all terms and iterate over them
            for term in document.terms:
                # If the term is not in the index, add it
                if term not in self.inverted_idx:
                    self.inverted_idx[term] = TermInfo(document, term)
                else:
                    # Otherwise append the document to the term
                    self.inverted_idx[term].append_document(document, term)

            # Add the document to the index
            self.documents[document.id] = document

        self._recalculate_models()

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
        document_id = document.id if document.id else self.get_next_doc_id()
        processable_text = document.text
        if document.title:  # title is optional so it may be None
            processable_text += ' ' + document.title
        logger.info(f'Preprocessing document id: {document_id}')
        document_tokens = self.config.preprocessor.get_tokens(processable_text)
        return Document(doc_id=document_id,
                        tokens=document_tokens,
                        title=document.title,
                        text=document.text, date=document.date if document.date is not None else datetime.now(),
                        additional_properties=document.additionalProperties)

    def preprocess_batch(self, documents: List[DocumentDto]):
        """
        Preprocesses batch of documents
        :param documents: List of DocumentDto objects
        :return: List of preprocessed Document objects
        """
        count = 0
        # noinspection PyTypeChecker
        result: List[Document] = [None] * len(documents)
        for i, document in enumerate(documents):
            result[i] = self.preprocess_document(document)
            logger.info('Preprocessed document id: %s', document.id)
            count += 1
            logger.info('Preprocessed %s documents', count)
        logger.info('Batch preprocessed, total documents in index: %s', len(self.documents))
        return result

    def delete_batch(self, documents: List[str]):
        """
        Deletes batch of documents from the index. Ignores any nonexistent ids
        :param documents: List of all documents to be deleted
        :return:
        """
        # Iterate over the list
        for document_id in documents:
            if document_id not in self.documents:
                # Skip the id if it does not exist
                logger.info(f'Document with id {document_id} does not exist in the index')
                continue

            document = self.documents[document_id]  # get the document
            del self.documents[document_id]  # delete the key

            # Iterate over the terms and delete the document from the term
            for term in document.terms:
                if term not in self.inverted_idx:
                    # This should not happen unless the index is corrupt
                    logger.error(f'Term {term} does not exist in the index')
                    continue

                term_info = self.inverted_idx[term]  # get reference to the term info
                term_info.remove_document(document_id)  # remove the linked document from the term
                if term_info.is_empty():
                    # If the term info is empty delete it
                    del self.inverted_idx[term]  # delete the term from the dictionary

        self._recalculate_models()
        logger.info(f'Batch of {len(documents)} documents deleted')

    def delete_document(self, doc_id: str):
        """
        Deletes a single document from the index
        :param doc_id: Document to delete
        :return: None
        """
        self.delete_batch([doc_id])

    def search(self, query_dto: QueryDto) -> DocumentSearchResultDto:
        """
        Performs search_model on all models
        :param query_dto: QueryDto object
        :return: dictionary for json response
        """
        query, model, n_items = query_dto.query, query_dto.model, query_dto.topK
        # Model variant gets validated in the controller via Pydantic, so we can assume it's valid
        search_model = self.models[model.value]
        search_result = search_model.search(query, n_items)

        if model == ModelVariant.BOOL:
            return DocumentSearchResultDto(
                documents=[DocumentDto.from_domain_object(item) for item in search_result[0]],
                stopwords=search_result[1],
                totalDocuments=search_result[2]
            )

        # Otherwise all other models return list of dictionaries that contain the document domain object and score
        return DocumentSearchResultDto(
            documents=[DocumentDto.from_domain_object(item['document'], item['score']) for item in search_result[0]],
            totalDocuments=search_result[1]
        )

    def to_dto(self, n_example_docs=10) -> IndexDto:
        """
        Converts this to IndexDto
        :return: instance of IndexDto
        """
        n_example_docs = n_example_docs if len(self.documents) > n_example_docs else len(self.documents)
        example_docs = [DocumentDto.from_domain_object(doc) for doc in
                        list(self.documents.values())[:n_example_docs]]
        return IndexDto(
            name=self.config.name,
            models=list(self.models.keys()),
            nTerms=len(self.inverted_idx),
            nDocs=len(self.documents),
            exampleDocuments=example_docs
        )

    def get_preprocessed_document_from_dto(self, document_dto: DocumentDto) -> Document:
        """
        Converts DocumentDto to Document
        :param document_dto: DocumentDto object
        :return: Document object
        """
        return self.preprocess_document(document_dto)

    @staticmethod
    def _parse_document_from_dict(doc_dict: dict) -> DocumentDto:
        """
        Parses a document from a dictionary
        :param doc_dict:
        :return:
        """
        if 'text' not in doc_dict:
            raise ValueError('Document text cannot be empty')

        # Map to DocumentDto and let the index preprocess the text
        return DocumentDto(id=doc_dict['id'] if 'id' in doc_dict else None, text=doc_dict['text'],
                           additionalProperties={prop: val for prop, val in doc_dict.items() if prop != 'text'})

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
                doc = self.preprocess_document(self._parse_document_from_dict(json_data))
                self.add_document(doc)
                return [doc]
            elif isinstance(json_data, list):
                # Else we have an array of documents
                docs = [self._parse_document_from_dict(doc) for doc in json_data]
                docs = self.preprocess_batch(docs)
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
