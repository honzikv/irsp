import logging

from fastapi import APIRouter, UploadFile
from src.index.index import get_index

logger = logging.getLogger(__name__)

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
