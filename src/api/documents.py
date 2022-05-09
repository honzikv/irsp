import logging

from fastapi import APIRouter, UploadFile

from src.api.indices_dtos import DocumentDto
from src.index.index import get_index

logger = logging.getLogger(__name__)

# Router for documents
documents_router = APIRouter(
    prefix='/indices'
)


@documents_router.get('/{index_name}/documents/{document_id}')
def get_document(index_name: str, document_id: str):
    """
    Gets a document from an index
    :param index_name: Name of the index
    :param document_id: Id of the document
    :return: DocumentDto
    """
    index = get_index(index_name)
    if document_id not in index.documents:
        return {"message": f"Document with id {document_id} not found", "success": False}
    return {"success": True, "message": DocumentDto.from_domain_object(index.documents[document_id])}


@documents_router.post('/{index_name}/documents/files')
def add_document(index_name: str, dataFile: UploadFile):
    """
    Adds a document to an index
    :param index_name: Name of the index
    :param dataFile: File to add
    :return: message with success: true or false otherwise
    """
    try:
        index = get_index(index_name)  # get the index
        logger.info(f'Indexing new documents in index {index_name}')

        index.add_json_to_index(dataFile)  # add the file to the index
        return {"success": True, "message": f"Files were successfully added"}

    except ValueError as e:
        return {"success": False, "message": str(e)}


def _save_document(index_name, documentDto):
    """
    Saves a document to an index
    :param index_name:
    :param documentDto:
    :return:
    """
    try:
        index = get_index(index_name)  # get the index
        logger.info(f'Updating document {documentDto.id} in index {index_name}')

        document = index.get_document_from_dto(documentDto)
        index.update_document(document)  # update the document
        return {"success": True, "message": f"Document was successfully updated"}
    except ValueError as e:
        return {"success": False, "message": str(e)}


@documents_router.post('/{index_name}/documents/{document_id}')
def update_document(index_name: str, document_id: str, documentDto: DocumentDto):
    """
    Updates a document in an index
    :param index_name: Name of the index
    :param documentDto: Document to update
    :return: message with success: true or false otherwise
    """
    documentDto.id = document_id
    return _save_document(index_name, documentDto)


@documents_router.post('/{index_name}/documents')
def add_document(index_name: str, documentDto: DocumentDto):
    """
    Adds a document to an index
    :param index_name:
    :param documentDto:
    :return:
    """
    return _save_document(index_name, documentDto)


@documents_router.delete('/{index_name}/documents/{doc_id}')
def delete_document(index_name: str, doc_id: str):
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
        return {"success": False, "message": str(e)}

# @index_router.delete('/{index_name}/documents/batch')
# def delete_documents(index_name: str, doc_ids: List[int]):
#     """
#     Deletes a list of documents from an index
#     :param index_name: Name of the index
#     :param doc_ids: List of document IDs
#     :return: True if successful, False otherwise
#     """
#     try:
#         index = get_index(index_name)
#         index.delete_batch(doc_ids)
#         return {"success": True}
#     except ValueError as e:
#         return {"success": False, "message": str(e)}
