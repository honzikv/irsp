import logging.config

from fastapi import FastAPI

# Main script which launches the api
from starlette.middleware.cors import CORSMiddleware

from src.api.indices import indices_router

# Configure logging
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

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

logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    return {"message": "A simple information retrieval API"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


app.include_router(indices_router)

logger.info('API is running')
