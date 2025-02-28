from fastapi import FastAPI

from app.business_logic.users.router import router as router_users

app = FastAPI(title="KnowledgeDB Admin API", description="The official API for manipulating the DonSU "
                                                         "vector knowledge database.", version="1.0.0")


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(router_users)
