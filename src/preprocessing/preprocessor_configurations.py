# This module contains default preprocessor configurations
from src.preprocessing.preprocessing import PreprocessorConfig

czech_default_stemmer = PreprocessorConfig(
    lowercase=True,
    remove_punctuation=True,
    remove_stopwords=True,
    remove_accents=True,
    lang='cs',
    use_stemmer=True
)

czech_default_lemmatizer = PreprocessorConfig(
    lowercase=True,
    remove_punctuation=True,
    remove_stopwords=True,
    remove_accents=True,
    lang='cs',
    use_stemmer=False
)

english_default_stemmer = PreprocessorConfig(
    lowercase=True,
    remove_punctuation=True,
    remove_stopwords=True,
    remove_accents=True,
    lang='en',
    use_stemmer=True
)

english_default_lemmatizer = PreprocessorConfig(
    lowercase=True,
    remove_punctuation=True,
    remove_stopwords=True,
    remove_accents=True,
    lang='en',
    use_stemmer=False
)
