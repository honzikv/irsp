#%%
import nltk
import os
from nltk_dependencies import setup_dependencies

# Download dependencies if necessary
setup_dependencies()

# Configure NLTK - set the resource path to correct location
nltk_resources_dir = os.path.join(os.getcwd(), 'resources\\nltk\\')
nltk.data.path.append(nltk_resources_dir)
#%%
import json

from src.preprocessing.preprocessor_configurations import english_default_stemmer
from src.index.index import Index
from src.index.index_config import IndexConfig

# Load sample file
with open('resources/docs/english_documents.json', 'r') as f:
    documents = json.load(f)

documents
#%%
from src.preprocessing.preprocessing import Preprocessor
from src.index.index import add_index, delete_index

try:
    delete_index('test')
except:
    pass

# Create new index and add it to the app
index = Index(
    config=IndexConfig(
        name='test',
        preprocessor=Preprocessor(english_default_stemmer),
    ),
    initial_batch=[]
)

add_index('test', index)
#%%
# Map json documents to domain objects
docs_domain = []
for doc in documents:
    docs_domain.append(
        index._parse_document_from_dict(doc)
    )
index.add_batch(docs_domain)

len(index.documents)
#%%
from src.api.indices_dtos import QueryDto, ModelVariant

# A simple boolean query
boolean_query = '(NOT (Are AND Are)) AND Fish tropical'
query_dto = QueryDto(query=boolean_query, model=ModelVariant.BOOL)

documents = index.search(query_dto)

for document in documents:
    print(document)