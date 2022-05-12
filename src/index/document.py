import uuid
from datetime import datetime
from typing import List, Union
import numpy as np


class Document:
    """
    Base interface to represent any document that can be indexed.
    Any document that can be indexed should implement this interface.
    """

    def __init__(self, doc_id: str, tokens: List[str], title: Union[str, None], text: str,
                 date: datetime = datetime.now(),
                 additional_properties: {} = None):
        """
        Initializes the document object
        :param doc_id: the document id
        :param tokens: tokens of the document obtained from preprocessing
        :param text: text of the document
        :param date: date the document was indexed
        :param additional_properties: additional properties
        """
        if additional_properties is None:
            additional_properties = {}
        self.id = doc_id
        self.title = title
        self.text = text
        self.date = date
        # bag of words (dictionary of term: frequency in the document)
        # bag of words has precalculated log tf values
        self.bow = Document.calculate_bow(tokens)
        self.properties = additional_properties

    @property
    def terms(self):
        """
        Returns the list of terms in the document
        :return:
        """
        return list(self.bow.keys())

    def __str__(self):
        return f'Document:\n\tid: {self.id}\n\ttokens: {self.terms}'

    @staticmethod
    def calculate_bow(tokens: List[str]):
        """
        Returns the bag of words representation of the document
        This property is lazy initialized
        :return:
        """
        bow = {}
        for token in tokens:
            if token not in bow:
                bow[token] = 1
            else:
                bow[token] += 1
        for token in bow:
            bow[token] = 1 + np.log(bow[token])
        return bow

