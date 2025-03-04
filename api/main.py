from fastapi import FastAPI

from app.business_logic.users.router import router as router_users
from app.business_logic.documents.router import router as router_documents

app = FastAPI(title="KnowledgeDB Admin API", description="The official API for manipulating the DonSU "
                                                         "vector knowledge database.", version="1.0.0")

app.include_router(router_users)
app.include_router(router_documents)
