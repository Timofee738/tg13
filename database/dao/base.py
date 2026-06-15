from database.connect import async_session

from sqlalchemy import select, insert

class BaseDao:
    model = None
    
    @classmethod
    async def find_one_or_none(cls, **filter):
        async with async_session() as session:
            query = select(cls.model).where(**filter)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def add(cls, **data):
        async with async_session() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()
            
            return
        