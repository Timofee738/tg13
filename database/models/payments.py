from database.connect import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, ForeignKey, DateTime, Numeric, func

from datetime import datetime

class Payments(Base):
    __tablename__ = "payments"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.tg_id", ondelete="CASCADE"))
    
    amount: Mapped[int] = mapped_column(Numeric(10, 2))
    
    time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    