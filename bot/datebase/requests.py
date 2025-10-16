from bot.datebase.models import async_session
from bot.datebase.models import User, Slot

from sqlalchemy import select, update, delete

from typing import Any


async def get_user(tg_id: int) -> User|Any:
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))

async def add_user(tg_id: int, name: str, phonenumber: str, isAdmin) -> None:
    async with async_session() as session:
        session.add(User(tg_id=tg_id, name=name, phonenumber=phonenumber, isAdmin=isAdmin))
        await session.commit()

async def update_name_user(tg_id, new_name) -> None:
    async with async_session() as session:
        stmt = update(User).where(User.tg_id == tg_id).values(name=new_name)

        await session.execute(stmt)
        await session.commit()

async def change_mode_user(tg_id) -> None:
    async with async_session() as session:
        stmt = update(User).where(User.tg_id == tg_id).values(mode=~User.mode)

        await session.execute(stmt)
        await session.commit()

async def get_slots(date: str) -> list[Slot]:
    async with async_session() as session:
        slot = (await session.scalars(select(Slot).where(Slot.date == date))).all()
        
        return slot

async def add_slot(date, time):
    async with async_session() as session:
        session.add(Slot(date=date, time=time))
        await session.commit()

async def get_all_slots():
    async with async_session() as session:
        return (await session.scalars(select(Slot))).all()
    
async def delete_slot(date, time):
    async with async_session() as session:
        stmt = delete(Slot).where((Slot.date == date) and (Slot.time == time))

        await session.execute(stmt)
        await session.commit()



# async def updates_all_slots()










