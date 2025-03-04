from fastapi import UploadFile
from pydantic import BaseModel


class DocumentUploadDTO(BaseModel):
    document: UploadFile
