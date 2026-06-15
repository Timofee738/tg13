from aiogram import Router

from src.bot.handlers.users import users_router


def get_handlers_router() -> Router:
    main_router = Router()
    


    main_router.include_routers(
        users_router
    )

    return main_router