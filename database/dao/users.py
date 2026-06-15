from database.dao.base import BaseDao

from database.models.users import Users

class UsersDao(BaseDao):
    model = Users