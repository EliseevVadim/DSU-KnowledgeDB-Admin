from sqlalchemy import select, func, or_, cast, String

from app.base_dao import BaseDAO
from app.business_logic.documents.models import Document
from app.database import async_session_maker


class DocumentsDAO(BaseDAO):
    model = Document

    @classmethod
    async def find_all_paginated(cls, limit: int = 10, offset: int = 0, search_query: str = None, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by).limit(limit).offset(offset)
            if search_query:
                search_pattern = f"%{search_query.lower()}%"
                query = query.filter(
                    or_(
                        func.lower(cast(cls.model.cmetadata["filename"], String)).ilike(search_pattern),
                        func.lower(cast(cls.model.cmetadata["source"], String)).ilike(search_pattern)
                    )
                )
            result = await session.execute(query)
            items = result.scalars().all()

            count_query = select(func.count()).select_from(cls.model).filter_by(**filter_by)
            if search_query:
                count_query = count_query.filter(
                    or_(
                        func.lower(cast(cls.model.cmetadata["filename"], String)).ilike(search_pattern),
                        func.lower(cast(cls.model.cmetadata["source"], String)).ilike(search_pattern)
                    )
                )
            total_result = await session.execute(count_query)
            total = total_result.scalar()
        return items, total


