import logging

from fastapi import APIRouter, UploadFile
from src.index.index import get_index

logger = logging.getLogger(__name__)

# Router for documents
documents_router = APIRouter(
    prefix='/indices'
)


@documents_router.post('/{index_name}/documents')
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
