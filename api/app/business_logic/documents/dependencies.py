import torch
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter
from transformers import AutoTokenizer, AutoModel

from app.config import get_model_name, get_connection_string, get_collection_name, get_model_revision
from app.utils.embeddings import get_embeddings

model_name_or_path = get_model_name()
model_revision = get_model_revision()

connection_string = get_connection_string()
collection_name = get_collection_name()

device = 'cuda' if torch.cuda.is_available() else 'cpu'

tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
model = AutoModel.from_pretrained(model_name_or_path,
                                  trust_remote_code=True,
                                  device_map=device, revision=model_revision)

embeddings = get_embeddings(model)

vector_db = PGVector.from_existing_index(
    embedding=embeddings,
    connection=connection_string,
    collection_name=collection_name
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=200,
    separators=["\n\n", "\n", " ", ""],
    add_start_index=True,
    length_function=lambda text: len(tokenizer.encode(text, add_special_tokens=False))
)


def get_vector_db() -> PGVector:
    return vector_db


def get_splitter() -> RecursiveCharacterTextSplitter:
    return splitter
