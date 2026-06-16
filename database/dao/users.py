from database.dao.base import BaseDao

from sqlalchemy import select

from database.models.users import Users
from database.connect import async_session

class UsersDao(BaseDao):
    model = Users
    
    
    @classmethod
    async def get_admins_id(cls):
        async with async_session() as session:
            query = select(Users.tg_id).where(Users.is_admin == True)
            result = await session.execute(query)
            
            return result.scalars().all()