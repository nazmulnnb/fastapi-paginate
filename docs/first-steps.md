It's pretty easy to use `fastapi-paginate`.

First, you need to import `Page`, `Params` and one of `paginate`
functions from `fastapi_paginate`.

* `Page` - is used as `response_model` in your route declaration.
* `Params` - is a user provide params for pagination.
* `paginate` - is a function that will paginate your data.


```python
from fastapi_pagination import Page, paginate, add_pagination
from fastapi import FastAPI
from pydantic import BaseModel


class User(BaseModel):
    name: str


app = FastAPI()

users = [
    User(name="Yurii"),
    # ...
]


@app.get(
    "/",
    response_model=Page[User],
)
async def route():
    return paginate(users)


add_pagination(app)
```
