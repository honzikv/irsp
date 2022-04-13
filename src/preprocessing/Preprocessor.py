import unicodedata

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


supported_langs = ['en', 'cs']

class PreprocessorConfig:

    def __init__(self,
                 lowercase: bool,
                 remove_accents: bool,
                 remove_stopwords: bool,
                 use_stemmer: bool,
                 lang: str,
                 ):
        """
        Configuration for preprocessor
        :param lowercase: lowercase all words
        :param remove_accents: remove accents
        :param remove_stopwords: remove stopwords
        :param use_stemmer: use stemmer if this is set to false lemmatizer will be used instead
        :param lang: language of the text
        """
        self.lowercase = lowercase
        self.remove_accents = remove_accents
        self.remove_stopwords = remove_stopwords
        self.use_stemmer = use_stemmer
        self.lang = lang


class Preprocessor:

    def __init__(self, config: PreprocessorConfig):
        self.config = config

    def get_terms(self, text: str) -> list:
        """
        Returns all terms found in the text
        :param text: text to be processed
        :return: list of terms
        """

        # lowercase
        if self.config.lowercase:
            text = text.lower()

        # remove accents
        if self.config.remove_accents:
            text = self.remove_accents(text)

        # tokenize
        text = word_tokenize(text, language=self.config.lang)

        # remove stopwords
        if self.config.remove_stopwords:
            text = self.remove_stopwords(text)

        if self.config.use_stemmer:


        return text

    @staticmethod
    def remove_accents(text: str) -> str:
        """
        Removes accents from the text
        :param text: text to be processed
        :return: text without accents
        """
        text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8', 'ignore')
        return text

    def remove_stopwords(self, text: list) -> list:
        """
        Removes stopwords from the text
        :param text: text to be processed
        :return: text without stopwords
        """
        return [word for word in text if word not in stopwords.words(self.config.lang)]
