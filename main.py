import logging.config
import os
import nltk
from fastapi import FastAPI

# Main script which launches the api
from starlette.middleware.cors import CORSMiddleware

from nltk_dependencies import setup_dependencies
from src.api.indices import indices_router

# Download dependencies
setup_dependencies()

# Configure logging
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

logger = logging.getLogger(__name__)

# Configure NLTK - set the resource path to correct location
nltk_resources_dir = os.path.join(os.getcwd(), 'resources\\nltk\\')
nltk.data.path.append(nltk_resources_dir)
logger.info(f'NLTK resources directory set to: {nltk_resources_dir}')

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


app.include_router(indices_router)

logger.info('API is running')
