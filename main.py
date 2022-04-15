from fastapi import FastAPI

# Main script which launches the api

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "A simple information retrieval API"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
