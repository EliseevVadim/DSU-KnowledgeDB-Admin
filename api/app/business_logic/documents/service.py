import os.path
import shutil

from fastapi import UploadFile
from langchain_community.document_loaders import UnstructuredFileLoader

from app.config import get_upload_dir


def save_file_temporarily(file: UploadFile):
    full_path = os.path.join(get_upload_dir(), file.filename)
    with open(full_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    return full_path


def extract_chunks_from_file(file_path: str, splitter):
    loader = UnstructuredFileLoader(file_path, encoding='utf-8')
    documents = loader.load_and_split(splitter)
    return documents
