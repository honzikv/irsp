# This module contains default preprocessor configurations
from src.preprocessing.preprocessing import PreprocessorConfig

czech_default_stemmer = PreprocessorConfig(
    lowercase=True,
    remove_punctuation=True,
    remove_stopwords=True,
    remove_accents_before_stemming=True,
    lang='cs',
    use_stemmer=True,
    remove_accents_after_stemming=True
)

czech_default_lemmatizer = PreprocessorConfig(
    lowercase=True,
    remove_punctuation=True,
    remove_stopwords=True,
    remove_accents_before_stemming=True,
    lang='cs',
    use_stemmer=False,
    remove_accents_after_stemming=True
)

english_default_stemmer = PreprocessorConfig(
    lowercase=True,
    remove_punctuation=True,
    remove_stopwords=True,
    remove_accents_before_stemming=True,
    lang='en',
    use_stemmer=True,
    remove_accents_after_stemming=True
)

english_default_lemmatizer = PreprocessorConfig(
    lowercase=True,
    remove_punctuation=True,
    remove_stopwords=True,
    remove_accents_before_stemming=True,
    lang='en',
    use_stemmer=False,
    remove_accents_after_stemming=True
)

