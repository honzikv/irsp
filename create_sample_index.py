import json

from src.preprocessing.preprocessor_configurations import english_default_stemmer
from src.index.index import Index
from src.index.index_config import IndexConfig
from src.preprocessing.preprocessing import Preprocessor
from src.index.index import add_index, delete_index


# Creates a dummy index
def create_dummy_idx():
    # Load sample file
    with open('resources/docs/english_documents.json', 'r') as f:
        documents = json.load(f)

    try:
        delete_index('dummyIdx')
    except:
        pass

    # Create new index and add it to the app
    index = Index(
        config=IndexConfig(
            name='dummyIdx',
            preprocessor=Preprocessor(english_default_stemmer),
        ),
        initial_batch=[]
    )

    # Map json documents to domain objects
    docs_domain = []
    for doc in documents:
        docs_domain.append(
            index._parse_document_from_dict(doc)
        )
    index.add_batch(docs_domain)

    add_index('dummyIdx', index)
