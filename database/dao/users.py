from database.dao.base import BaseDao

from sqlalchemy import select, func

from database.models.users import Users
from database.connect import async_session

from datetime import timedelta, datetime, timezone

class UsersDao(BaseDao):
    model = Users
    
    
    
    
    
    #ADMINS
    @classmethod
    async def get_admins_id(cls):
        async with async_session() as session:
            query = select(Users.tg_id).where(Users.is_admin == True)
            result = await session.execute(query)
            
            return result.scalars().all()
        
    @classmethod
    async def count_users(cls):
        async with async_session() as session:
            query = select(func.count(Users.tg_id))
            result = await session.execute(query)
            return result.scalar() or 0
        
    @classmethod
    async def count_day_users(cls):
        async with  async_session() as session:
            day = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=1)
            
            query = select(func.count(Users.tg_id)).where(Users.created_at >= day)
            result = await session.execute(query)
            return result.scalar() or 0