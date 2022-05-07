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
    docId: Optional[uuid.UUID]
    text: str
    # Additional properties to the document
    additionalProperties: dict

    @staticmethod
    def from_domain_object(document: Document):
        """
        Converts a Document object to a DTO
        :param document: Document object
        :return: DocumentDto
        """
        return DocumentDto(
            docId=document.doc_id,
            text=document.text,
            additionalProperties=document.properties,
        )


class IndexDto(Model):
    """
    Data transfer object for an index
    """
    name: str
    models: List[str]
    nTerms: int
    nDocs: int
    exampleDocuments: List[DocumentDto]


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
    query: str
    topK: Optional[int]
    model: ModelVariant
