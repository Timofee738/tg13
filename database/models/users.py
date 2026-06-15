from database.connect import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, func

from datetime import datetime

class Users(Base):
    __tablename__ = "users"
    
    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    
    username: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    
    is_admin: Mapped[bool] = mapped_column(default=False)