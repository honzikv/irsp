import json

from src.preprocessing.preprocessor_configurations import english_default_stemmer, czech_default_stemmer
from src.index.index import Index
from src.index.index_config import IndexConfig
from src.preprocessing.preprocessing import Preprocessor
from src.index.index import add_index, delete_index


# Creates a dummy index
def create_dummy_idx():
    # Load sample file
    with open('resources/docs/english_documents.json', 'r') as f:
        documents_en = json.load(f)

    with open('resources/docs/czech_documents.json', 'r', encoding='utf8') as f:
        documents_cs = json.load(f)

    try:
        delete_index('dummyIdxEn')
        delete_index('dummyIdxCs')
    except:
        pass

    # Create new index and add it to the app
    index_en = Index(
        config=IndexConfig(
            name='dummyIdxEn',
            preprocessor=Preprocessor(english_default_stemmer),
        ),
        initial_batch=[]
    )

    index_cs = Index(
        config=IndexConfig(
            name='dummyIdxCs',
            preprocessor=Preprocessor(czech_default_stemmer)
        ),
        initial_batch=[]
    )

    # Map json documents to domain objects
    docs_domain = []
    for doc in documents_en:
        docs_domain.append(
            index_en.preprocess_document(index_en._parse_document_from_dict(doc))
        )
    index_en.add_batch(docs_domain)

    docs_domain.clear()
    for doc in documents_cs:
        docs_domain.append(
            index_cs.preprocess_document(index_cs._parse_document_from_dict(doc))
        )
    index_cs.add_batch(docs_domain)

    add_index('dummyIdxEn', index_en)
    add_index('dummyIdxCs', index_cs)
