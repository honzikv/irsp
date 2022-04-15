from typing import List

from fastapi import APIRouter

from src.api.indices_dtos import DocumentDto, IndexConfigDto
from src.index.index import add_index, Index, delete_index, get_index
from src.index.index import get_all_indices as _get_all_indices

# API router to set endpoints for indexing
indices_router = APIRouter(
    prefix='/indices'
)


@indices_router.post('/{name}')
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


@indices_router.delete('/{name}')
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


@indices_router.post('/{index_name}/documents')
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


@indices_router.post('/{index_name}/documents/batch')
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


@indices_router.delete('/{index_name}/documents/{doc_id}')
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


@indices_router.delete('/{index_name}/documents/batch')
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


@indices_router.get('/')
def get_all_indices():
    """
    Returns all indices
    :return: List of indices
    """
    return {"success": True, "message": _get_all_indices()}
