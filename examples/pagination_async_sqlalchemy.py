from typing import Any, AsyncIterator

import uvicorn
from faker import Faker
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from fastapi_paginate import Page, add_pagination
from fastapi_paginate.ext.async_sqlalchemy import paginate

faker = Faker()

engine = create_async_engine("sqlite+aiosqlite:///.db")
async_session = sessionmaker(engine, class_=AsyncSession)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)


class UserIn(BaseModel):
    name: str
    email: str


class UserOut(UserIn):
    id: int

    class Config:
        orm_mode = True


app = FastAPI()


@app.on_event("startup")
async def on_startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        session.add_all([User(name=faker.name(), email=faker.email()) for _ in range(100)])
        await session.commit()


async def get_db() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session


@app.post("/users", response_model=UserOut)
async def create_user(user_in: UserIn, db: AsyncSession = Depends(get_db)) -> User:
    user = User(name=user_in.name, email=user_in.email)
    db.add(user)
    await db.flush()

    return user


@app.get("/users/default", response_model=Page[UserOut])
async def get_users(db: AsyncSession = Depends(get_db)) -> Any:
    return await paginate(db, select(User))


add_pagination(app)

if __name__ == "__main__":
    uvicorn.run("pagination_async_sqlalchemy:app")
