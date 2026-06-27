from database.connect import async_session

from sqlalchemy import select, insert, update

class BaseDao:
    model = None
    
    @classmethod
    async def find_one_or_none(cls, **filter):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def add(cls, **data):
        async with async_session() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()
            
            return
        
    @classmethod
    async def edit_data(cls, filter_by: dict, **data):
        async with async_session() as session:
            query = (
                update(cls.model)
                .filter_by(**filter_by)
                .values(**data)
                .returning(cls.model)
            )
            result = await session.execute(query)
            await session.commit()
            
            return result.scalar_one_or_none()
        