from typing import List

from fastapi import APIRouter
from pydantic.class_validators import Optional
from pydantic.main import Model

from src.index.index import add_index, IndexConfig, Index, delete_index, get_index

# Module for controlling indices
from src.preprocessing.preprocessing import PreprocessorConfig, Preprocessor

router = APIRouter()


class PreprocessorConfigDto(Model):
    """
    Preprocessor configuration DTO
    """
    lowercase: bool
    removeAccentsBeforeStemming: bool
    removePunctuation: bool
    removeStopwords: bool
    useStemmer: bool
    lang: str
    removeAccentsAfterStemming: bool

    def to_domain_object(self):
        """
        Converts the DTO to a PreprocessorConfig object
        :return: PreprocessorConfig object
        """
        return PreprocessorConfig(
            lowercase=self.lowercase,
            remove_accents_before_stemming=self.removeAccentsBeforeStemming,
            remove_punctuation=self.removePunctuation,
            remove_stopwords=self.removeStopwords,
            use_stemmer=self.useStemmer,
            lang=self.lang,
            remove_accents_after_stemming=self.removeAccentsAfterStemming,
        )


class IndexConfigDto(Model):
    """
    Index configuration DTO
    """
    name: str
    models: List[str]
    preprocessorConfig: PreprocessorConfigDto

    def to_domain_object(self):
        """
        Converts the DTO to an IndexConfig object
        :return: IndexConfig
        """
        return IndexConfig(
            name=self.name,
            models=self.models,
            preprocessor=Preprocessor(self.preprocessorConfig.to_domain_object()),
        )


class DocumentDto(Model):
    """
    Document DTO
    """
    docId: Optional[str]
    text: str
    # Additional properties to the document
    additionalProperties: {}


@router.post('/index/{name}')
def create_idx(name: str, index_config: IndexConfigDto):
    """
    Creates an index
    :param name: Name of the index
    :param index_config: Index configuration
    :return: True if successful, False otherwise
    """
    try:
        add_index(name, Index(index_config.to_domain_object(), []))
        return {"success": True}
    except ValueError as e:
        return {"success": False, "error": str(e)}


@router.delete('/index/{name}')
def delete_idx(name: str):
    """
    Deletes an index
    :param name: Name of the index
    :return: True if successful, False otherwise
    """
    try:
        delete_index(name)
        return {"success": True}
    except ValueError as e:
        return {"success": False, "error": str(e)}


@router.post('/index/{index_name}/documents')
def add_document(index_name: str, document: DocumentDto):
    """
    Adds a document to an index
    :param index_name:  Name of the index
    :param document: Document to add
    :return: True if successful, False otherwise
    """
    try:
        index = get_index(index_name)
        document = index.preprocess_document(document)
        index.add_document(document)
        return {"success": True}
    except ValueError as e:
        return {"success": False, "error": str(e)}


@router.post('/index/{index_name}/documents/batch')
def add_documents(index_name: str, documents: List[DocumentDto]):
    """
    Adds a list of documents to an index
    :param index_name:  Name of the index
    :param documents: List of documents to add
    :return: True if successful, False otherwise
    """
    try:
        index = get_index(index_name)
        documents = index.preprocess_batch(documents)
        index.add_batch(documents)
        return {"success": True}
    except ValueError as e:
        return {"success": False, "error": str(e)}


@router.delete('/index/{index_name}/documents/{doc_id}')
def delete_document(index_name: str, doc_id: int):
    """
    Deletes a document from an index
    :param index_name: Name of the index
    :param doc_id: Document ID
    :return: True if successful, False otherwise
    """
    try:
        index = get_index(index_name)
        index.delete_document(doc_id)
        return {"success": True}
    except ValueError as e:
        return {"success": False, "error": str(e)}


@router.delete('/index/{index_name}/documents/batch')
def delete_documents(index_name: str, doc_ids: List[int]):
    """
    Deletes a list of documents from an index
    :param index_name: Name of the index
    :param doc_ids: List of document IDs
    :return: True if successful, False otherwise
    """
    try:
        index = get_index(index_name)
        index.delete_batch(doc_ids)
        return {"success": True}
    except ValueError as e:
        return {"success": False, "error": str(e)}
