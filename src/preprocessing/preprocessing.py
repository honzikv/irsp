import unicodedata
import nltk

from nltk import WordNetLemmatizer, SnowballStemmer, PorterStemmer, word_tokenize
from nltk.corpus import stopwords
from src.preprocessing.czech_lemmatizer import CzechLemmatizer
from src.preprocessing.czech_stemmer import CzechStemmer

# Download wordnet and omw-1.4 for lemmatization
nltk.download('wordnet')
nltk.download('omw-1.4')

supported_langs = ['en', 'cs']

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
                 remove_accents: bool,
                 remove_punctuation: bool,
                 remove_stopwords: bool,
                 use_stemmer: bool,
                 lang: str
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
        self.remove_punctuation = remove_punctuation
        self.remove_stopwords = remove_stopwords
        self.use_stemmer = use_stemmer
        self.lang = lang

        if lang not in supported_langs:
            raise ValueError('Language not supported')

class Preprocessor:

    def __init__(self, config: PreprocessorConfig):
        self.config = config
        self.stemmer = stemmers[self.config.lang]
        self.lemmatizer = lemmatizers[self.config.lang]

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

        # remove punctuation
        if self.config.remove_punctuation:
            text = text.translate(str.maketrans('', '', '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'))

        # tokenize
        text = word_tokenize(text, language=self.config.lang)

        # remove stopwords
        if self.config.remove_stopwords:
            text = self.remove_stopwords(text)

        # use stemmer or lemmatizer
        text = self.stemmer.stem(text) if self.config.use_stemmer else self.lemmatizer.lemmatize(text)

        return text

    @staticmethod
    def remove_accents(text: str) -> str:
        """
        Removes accents from the text
        :param text: text to be processed
        :return: text without accents
        """
        text = unicodedata.normalize('NFKD', text).encode(
            'ASCII', 'ignore').decode('utf-8', 'ignore')
        return text

    def remove_stopwords(self, text: list) -> list:
        """
        Removes stopwords from the text
        :param text: text to be processed
        :return: text without stopwords
        """
        return [word for word in text if word not in stopwords.words(self.config.lang)]

