from aiogram import Router

from src.bot.handlers.users import users_router
from src.bot.handlers.admins import admin_router

from src.bot.midlewares.admin import AdminMiddleware

from database.dao.users import UsersDao


async def get_handlers_router() -> Router:
    main_router = Router()
    
    try:
        admins = await UsersDao.get_admins_id()
        set_ids = set(admins)
    except Exception as e:
        print(f"Error: {e}")
        set_ids = set()
    
    admin_router.message.middleware(AdminMiddleware(admin_ids=set_ids))
    admin_router.callback_query.middleware(AdminMiddleware(admin_ids=set_ids))
    


    main_router.include_routers(
        users_router,
        admin_router
    )

    return main_router