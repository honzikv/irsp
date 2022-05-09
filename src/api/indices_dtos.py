from datetime import datetime
import uuid
from enum import Enum

from pydantic.class_validators import Optional, List
from pydantic.main import BaseModel as Model

from src.index.document import Document
from src.index.index_config import IndexConfig
from src.preprocessing.preprocessing import PreprocessorConfig, Preprocessor


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
    preprocessorConfig: PreprocessorConfigDto

    def to_domain_object(self):
        """
        Converts the DTO to an IndexConfig object
        :return: IndexConfig
        """
        return IndexConfig(
            name=self.name,
            preprocessor=Preprocessor(self.preprocessorConfig.to_domain_object()),
        )


class DocumentDto(Model):
    """
    Document DTO
    """
    title: Optional[str]
    id: Optional[str]
    date: Optional[datetime]
    text: str
    # Additional properties to the document
    additionalProperties: dict
    score: Optional[float]

    @staticmethod
    def from_domain_object(document: Document, score: Optional[float] = None):
        """
        Converts a Document object to a DTO
        :param document: Document object
        :param score: score of the document
        :return: DocumentDto
        """
        return DocumentDto(
            id=document.id,
            text=document.text,
            title=document.title,
            date=document.date,
            additionalProperties=document.properties,
            score=score,
        )


class DocumentSearchResultDto(Model):
    documents: List[DocumentDto]
    stopwords: Optional[List[str]]


class IndexDto(Model):
    """
    Data transfer object for an index
    """
    name: str  # name of the index
    nTerms: int  # number of terms in the index
    nDocs: int  # number of documents in the index
    exampleDocuments: List[DocumentDto]  # list of example documents


class ModelVariant(Enum):
    """
    Enum for model variants
    """
    TFIDF = 'tfidf'
    BOOL = 'bool'
    TRANSFORMERS = 'transformers'


class QueryDto(Model):
    """
    Data transfer object for query
    """
    query: str  # query string
    topK: Optional[int]  # number of results to return
    model: ModelVariant  # model variant
