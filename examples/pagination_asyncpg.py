from typing import Any

import uvicorn
from asyncpg import Pool, create_pool
from faker import Faker
from fastapi import FastAPI
from pydantic import BaseModel

from fastapi_paginate import Page, add_pagination
from fastapi_paginate.ext.asyncpg import paginate

faker = Faker()


class UserIn(BaseModel):
    name: str
    email: str


class UserOut(UserIn):
    id: int

    class Config:
        orm_mode = True


app = FastAPI()
pool: Pool


@app.on_event("startup")
async def on_startup() -> None:
    global pool
    pool = await create_pool("postgresql://postgres:postgres@localhost:5432")

    async with pool.acquire() as conn:
        await conn.fetch("""DROP TABLE IF EXISTS users;""")
        await conn.fetch(
            """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        );
        """
        )

        for _ in range(100):
            await conn.fetch(
                """INSERT INTO users (name, email) VALUES($1, $2) RETURNING (id, name, email)""",
                faker.name(),
                faker.email(),
            )


@app.post("/users", response_model=UserOut)
async def create_user(user_in: UserIn) -> Any:
    async with pool.acquire() as conn:
        entity = await conn.fetch(
            """INSERT INTO users (name, email) VALUES($1, $2) RETURNING (id, name, email)""",
            user_in.name,
            user_in.email,
        )
        return {**entity}


@app.get("/users/default", response_model=Page[UserOut])
async def get_users() -> Any:
    async with pool.acquire() as conn:
        return await paginate(conn, """SELECT id, name, email FROM users WHERE id=$1""")


add_pagination(app)

if __name__ == "__main__":
    uvicorn.run("pagination_asyncpg:app")
