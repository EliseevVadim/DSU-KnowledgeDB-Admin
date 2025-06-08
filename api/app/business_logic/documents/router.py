import os
from typing import Optional

from fastapi import APIRouter, Depends, Query, UploadFile, File

from app.business_logic.documents.dao import DocumentsDAO
from app.business_logic.documents.dependencies import get_vector_db, get_splitter
from app.business_logic.documents.service import save_file_temporarily, extract_chunks_from_file
from app.business_logic.users.dependencies import get_user
from app.business_logic.users.models import User

from datetime import datetime

router = APIRouter(prefix='/documents', tags=['Documents'])


@router.get('/')
async def get_all_documents(user_data: User = Depends(get_user),
                            limit: int = Query(10, ge=1, le=25, description="Количество записей на странице"),
                            offset: int = Query(0, ge=0, description="Смещение записей"),
                            query: Optional[str] = Query(None, description="Поисковый запрос по названию файла")):
    documents, total = await DocumentsDAO.find_all_paginated(limit=limit, offset=offset, search_query=query)
    return {'documents': documents, 'total': total}


@router.post('/upload')
async def upload_document(user_data: User = Depends(get_user),
                          file: UploadFile = File(..., description='Векторизуемый файл'),
                          splitter=Depends(get_splitter),
                          vector_db=Depends(get_vector_db)):
    file_path = save_file_temporarily(file)
    documents = extract_chunks_from_file(file_path, splitter)
    documents_count = len(documents)
    for document in documents:
        document.metadata['filename'] = os.path.splitext(file.filename)[0]
        document.metadata['last_updated'] = datetime.now().strftime("%d-%m-%Y")
    vector_db.add_documents(documents)
    os.remove(file_path)
    return {'ok': True, 'path': file_path, 'count': documents_count}


@router.delete('/{document_id}')
async def delete_document(document_id: str,
                          vector_db=Depends(get_vector_db)):
    vector_db.delete(ids=[document_id])
    return {'ok': True, 'message': 'Документ был успешно удален'}
