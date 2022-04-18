# FastAPI Pagination

FastAPI Pagination - easy to use pagination for FastAPI.

Example of code and generated OpenAPI specification.

```python
from fastapi import FastAPI
from pydantic import BaseModel

from fastapi_paginate import Page, add_pagination, paginate

app = FastAPI()


class User(BaseModel):
    name: str
    surname: str


users = [
    User(name='Yurii', surname='Karabas'),
    # ...
]


@app.get('/users', response_model=Page[User])
async def get_users():
    return paginate(users)


add_pagination(app)
```

![OpenAPI](img/openapi_example.png)

## Available integrations

* [sqlalchemy](https://github.com/sqlalchemy/sqlalchemy)
* [gino](https://github.com/python-gino/gino)
* [databases](https://github.com/encode/databases)
* [ormar](http://github.com/collerek/ormar)
* [orm](https://github.com/encode/orm)
* [tortoise](https://github.com/tortoise/tortoise-orm)

To see fully working examples, please visit this
[link](https://github.com/nazmulnnb/fastapi-paginate/tree/main/examples).

## Installation

```bash
# Basic version
pip install fastapi-paginate

# All available integrations
pip install fastapi-paginate[all]
```