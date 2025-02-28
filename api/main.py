from fastapi import FastAPI

app = FastAPI(title="KnowledgeDB Admin API", description="The official API for manipulating the DonSU "
                                                         "vector knowledge database.", version="1.0.0")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
