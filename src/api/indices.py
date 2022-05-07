import json
import logging
from typing import List

from fastapi import APIRouter, Form, UploadFile, File
from pydantic.class_validators import Optional

from src.api.indices_dtos import DocumentDto, IndexConfigDto, PreprocessorConfigDto, QueryDto
from src.index.index import add_index, Index, delete_index, get_index
from src.index.index import get_all_indices as _get_all_indices

# This module contains all the endpoints in the /indices path
# Since the app is very small some of the business logic is placed here instead of service layer

# API router to set endpoints for indexing
index_router = APIRouter(
    prefix='/indices'
)

logger = logging.getLogger(__name__)


@index_router.post('/{name}')
async def create_idx(name: str, idxConfig: str = Form(...), dataFile: Optional[UploadFile] = None):
    """
    Creates an index
    :param name: Name of the index
    :param idxConfig: json with configuration
    :param dataFile: File containing the docs to index - may be null
    :return: True if successful, False otherwise
    """
    try:
        preprocessor_config_dto = PreprocessorConfigDto(**json.loads(idxConfig))
        index_config_dto = IndexConfigDto(name=name, preprocessorConfig=preprocessor_config_dto)
        add_index(name, Index(index_config_dto.to_domain_object(), []))

        if not dataFile:
            # Process datafile if provided
            return {"success": True, "message": f"Index {name} was successfully created."}

        index = get_index(name)
        logger.info("Indexing docs file")
        documents = index.add_json_to_index(dataFile)
        return {"success": True,
                "message": f"Index {name} was successfully created with {len(documents)} documents.",
                "documents": documents}
    except ValueError as e:
        return {"success": False, "message": str(e)}


@index_router.delete('/{name}')
def delete_idx(name: str):
    """
    Deletes an index
    :param name: Name of the index
    :return: True if successful, False otherwise
    """
    try:
        delete_index(name)
        return {"success": True, "message": f"Index {name} was successfully deleted."}
    except ValueError as e:
        return {"success": False, "message": str(e)}


@index_router.post('/{index_name}/documents/batch')
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
        return {"success": False, "message": str(e)}


@index_router.get('/')
def get_all_indices():
    """
    Returns all indices
    :return: List of indices
    """
    return {"success": True, "message": _get_all_indices()}


@index_router.post('/{index_name}/search')
def search(index_name: str, query_dto: QueryDto):
    """
    Searches an index
    :param index_name: Name of the index
    :param query_dto: QueryDto object
    :return:
    """
    try:
        index = get_index(index_name)
        result = index.search(query_dto)
        return {"success": True, "message": result}
    except ValueError as e:
        return {"success": False, "message": str(e)}
