import logging.config
import os
import nltk
from fastapi import FastAPI

# Main script which launches the api
from starlette.middleware.cors import CORSMiddleware

from create_sample_index import create_dummy_idx

from src.api.documents import documents_router
from src.api.indices import index_router
from nltk_dependencies import setup_dependencies
# Download dependencies
setup_dependencies()

# Configure logging
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

logger = logging.getLogger(__name__)

# Configure NLTK - set the resource path to correct location
nltk_resources_dir = os.path.join(os.getcwd(), 'resources\\nltk\\')
nltk.data.path.append(nltk_resources_dir)
logger.info(f'NLTK resources directory set to: {nltk_resources_dir}')

# Create sample index
create_dummy_idx()

app = FastAPI()

# Add cors
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "A simple information retrieval API"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


app.include_router(index_router)
app.include_router(documents_router)

logger.info('API is running')
