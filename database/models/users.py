from database.connect import Base

from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, func, Date

from datetime import date

class Users(Base):
    __tablename__ = "users"
    
    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    
    username: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    
    created_at: Mapped[date] = mapped_column(default=func.now())
    
    is_active: Mapped[bool] = mapped_column(default=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=True)