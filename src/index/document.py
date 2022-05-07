import uuid
from datetime import datetime
from typing import List


class Document:
    """
    Base interface to represent any document that can be indexed.
    Any document that can be indexed should implement this interface.
    """

    def __init__(self, doc_id: uuid.UUID, tokens: List[str], text: str, date_added: datetime = datetime.now(),
                 additional_properties: {} = None):
        """
        Initializes the document object
        :param doc_id: the document id
        :param tokens: tokens of the document obtained from preprocessing
        :param text: text of the document
        :param date_added: date the document was indexed
        :param additional_properties: additional properties
        """
        if additional_properties is None:
            additional_properties = {}
        self.doc_id = doc_id
        self.tokens = tokens
        self.text = text
        self.date_added = date_added
        self.last_updated_at = date_added
        self._bow = None  # bag of words (dictionary of term: frequency in the document)
        self.properties = additional_properties

    def __str__(self):
        return f'Document:\n\tid: {self.doc_id}\n\ttokens: {self.tokens}'

    @property
    def bow(self):
        """
        Returns the bag of words representation of the document
        This property is lazy initialized
        :return:
        """
        if self._bow is None:
            bow = {}
            for token in self.tokens:
                if token not in bow:
                    bow[token] = 1
                else:
                    bow[token] += 1
            self._bow = bow
        return self._bow
