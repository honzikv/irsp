import nltk
import os
from nltk_dependencies import download_dependencies

# Download dependencies if necessary
import json

from src.api.indices_dtos import ModelVariant, QueryDto
from src.preprocessing.preprocessor_configurations import english_default_stemmer
from src.index.index import Index
from src.index.index_config import IndexConfig
from src.preprocessing.preprocessing import Preprocessor, SimplePreprocessor
from src.index.index import add_index, delete_index

download_dependencies()

# Configure NLTK - set the resource path to correct location
nltk_resources_dir = os.path.join(os.getcwd(), 'resources\\nltk\\')
nltk.data.path.append(nltk_resources_dir)

# Load sample file
with open('resources/docs/english_documents.json', 'r') as f:
    documents = json.load(f)


try:
    delete_index('test')
except:
    pass

# Create new index and add it to the app
index = Index(
    config=IndexConfig(
        name='test',
        preprocessor=SimplePreprocessor(),
    ),
    initial_batch=[]
)

add_index('test', index)

# Map json documents to domain objects
docs_domain = []
for doc in documents:
    docs_domain.append(
        index._parse_document_from_dict(doc)
    )
index.add_batch(docs_domain)

len(index.documents)

# Now test TF-IDF
tfidf_query = 'tropical fish sea'
query_dto = QueryDto(query=tfidf_query, model=ModelVariant.TFIDF)

documents = index.search(query_dto)

print(f'Found {len(documents)} documents')
for document in documents:
    print(document)
