import logging
import string
from typing import List, Tuple, Union

import unicodedata

from nltk import WordNetLemmatizer, PorterStemmer, word_tokenize
from nltk.corpus import stopwords
from src.preprocessing.czech_lemmatizer import CzechLemmatizer
from src.preprocessing.czech_stemmer import CzechStemmer

supported_langs = ['en', 'cs']
lang_full_mapping = {'en': 'english', 'cs': 'czech'}

logger = logging.getLogger(__name__)

# Supported stemmers
stemmers = {
    'en': PorterStemmer(),
    'cs': CzechStemmer()
}

# Supported lemmatizers
lemmatizers = {
    'en': WordNetLemmatizer(),
    'cs': CzechLemmatizer()
}


class PreprocessorConfig:

    def __init__(self,
                 lowercase: bool,
                 remove_accents_before_stemming: bool,
                 remove_punctuation: bool,
                 remove_stopwords: bool,
                 use_stemmer: bool,
                 lang: str,
                 remove_accents_after_stemming: bool
                 ):
        """
        Configuration for preprocessor
        :param lowercase: lowercase all words
        :param remove_accents_before_stemming: remove accents
        :param remove_stopwords: remove stopwords
        :param use_stemmer: use stemmer if this is set to false lemmatizer will be used instead
        :param lang: language of the text
        """
        self.lowercase = lowercase
        self.remove_accents = remove_accents_before_stemming
        self.remove_accents_after_stemming = remove_accents_after_stemming
        self.remove_punctuation = remove_punctuation
        self.remove_stopwords = remove_stopwords
        self.use_stemmer = use_stemmer
        self.lang = lang
        self.lang_full = lang_full_mapping[lang]

        if lang not in supported_langs:
            raise ValueError('Language not supported')


class SimplePreprocessor:
    """
    Simplest preprocessor implementation that only splits by whitespaces (used for debug)
    """

    def get_tokens(self, text: str) -> List[str]:
        """
        Returns tokens of the text
        :param text: text to tokenize
        :return: list of tokens
        """
        return text.split()


class Preprocessor:
    """
    Class for text preprocessing. Can split text into tokens / terms
    """

    def __init__(self, config: PreprocessorConfig):
        self.config = config
        self.stemmer = stemmers[self.config.lang]
        self.lemmatizer = lemmatizers[self.config.lang]
        self.stopwords = {
            'en': set(stopwords.words('english')),
            'cs': set(stopwords.words('czech'))
        }

    def get_tokens(self, text: str, return_detected_stopwords=False) -> Union[list, Tuple[list, set]]:
        """
        Returns all tokens found in the text
        :param text: text to be processed
        :return: list of terms
        :param return_detected_stopwords:
        """

        # Lowercase
        if self.config.lowercase:
            text = text.lower()

        # Remove accents
        if self.config.remove_accents:
            text = self._remove_accents(text)

        # Remove punctuation
        if self.config.remove_punctuation:
            text = text.translate(str.maketrans('', '', string.punctuation))

        # Tokenize
        text = word_tokenize(text, language=self.config.lang_full)

        # Remove stopwords
        detected_stopwords = set()  # this is only populated if return_detected_stopwords is set to True
        if self.config.remove_stopwords:
            if return_detected_stopwords:
                text, stopwords = self._remove_stopwords(text, return_detected_stopwords=True)
                detected_stopwords.update(stopwords)
            else:
                text = self._remove_stopwords(text)

        # Use stemmer or lemmatizer
        tokens = []
        for token in text:
            if self.config.use_stemmer:
                tokens.append(self.stemmer.stem(token))
            else:
                tokens.append(self.lemmatizer.lemmatize(token))

        if self.config.remove_accents_after_stemming:
            tokens = [self._remove_accents(token) for token in tokens]

        if return_detected_stopwords:
            # Return tuple of tokens and detected stopwords if return_detected_stopwords is set to True
            if len(detected_stopwords) != 0:
                logger.debug(f'Detected stopwords: {detected_stopwords}')
            return tokens, detected_stopwords

        # Otherwise just return list of tokens
        return tokens

    @staticmethod
    def _remove_accents(text: str) -> str:
        """
        Removes accents from the text
        :param text: text to be processed
        :return: text without accents
        """
        text = unicodedata.normalize('NFKD', text).encode(
            'ASCII', 'ignore').decode('utf-8', 'ignore')
        return text

    def _remove_stopwords(self, text: list, return_detected_stopwords=False) -> Union[list, Tuple[list, set]]:
        """
        Removes stopwords from the text
        :param text: text to be processed
        :param return_detected_stopwords: if true stopwords will be returned as well - the returned value will be a tuple
        with first element being the list of tokens and second element being the set of stopwords
        :return: text without stopwords
        """
        if return_detected_stopwords:
            tokens, detected_stopwords = [], []
            for token in text:
                if token in self.stopwords[self.config.lang]:
                    detected_stopwords.append(token)
                    continue
                tokens.append(token)
            return tokens, set(detected_stopwords)

        # Otherwise simply return only list of words that are not stopwords
        return [word for word in text if word not in self.stopwords[self.config.lang]]
