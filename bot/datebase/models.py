from sqlalchemy import BigInteger, String, Boolean, ForeignKey, DateTime, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from datetime import datetime

engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3")

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger, unique=True)
    name: Mapped[str] = mapped_column(String(16))
    phonenumber: Mapped[str] = mapped_column(String(12))
    isAdmin: Mapped[bool] = mapped_column(Boolean)
    mode: Mapped[bool] = mapped_column(Boolean)

    # bookings: Mapped[list["Booking"]] = relationship(back_populates="user")


# class Service(Base):
#     __tablename__ = "services"

#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
#     description: Mapped[str] = mapped_column(String(64), nullable=True)

#     slots: Mapped[list["Slot"]] = relationship(back_populates="service")


class Slot(Base):
    __tablename__ = "slots"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True) 
    data: Mapped[str] = mapped_column(DateTime)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)




# class Booking(Base):
#     __tablename__ = "bookings"

#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     tg_user_id = mapped_column(ForeignKey("users.tg_id"))    
#     slot_id: Mapped[int] = mapped_column(ForeignKey("slots.id"))
#     booked_at: Mapped[datetime] = mapped_column(DateTime, default=func.now)

#     __table_args__ = (UniqueConstraint("slot_id", name="uix_slot_id"),)



async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)