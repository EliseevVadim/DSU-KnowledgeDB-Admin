from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.business_logic.users.router import router as router_users
from app.business_logic.documents.router import router as router_documents

app = FastAPI(title="KnowledgeDB Admin API", description="The official API for manipulating the DonSU "
                                                         "vector knowledge database.", version="1.0.0")

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_users)
app.include_router(router_documents)
