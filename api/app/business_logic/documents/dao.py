from app.base_dao import BaseDAO
from app.business_logic.documents.models import Document


class DocumentsDAO(BaseDAO):
    model = Document
