You can use regular orm statement to paginate the results.
So, applying filters are same as you always did.

Here is an example for sqlalchemy

```python
from fastapi import FastAPI, Depends
from pydantic import BaseModel

from fastapi_paginate import Page, add_pagination
from fastapi_paginate.ext.sqlalchemy import paginate

from sqlalchemy.orm import Session

app = FastAPI()

class UserModel(Base):
    name = Column(String)
    surname = Column(String)
    age = Column(Integer)

class User(BaseModel):
    name: str
    surname: str
    age: int

@app.get('/users', response_model=Page[User])
async def get_users(db_session: Session = Depends(get_db_session)):
    stmt = db_session.query(UserModel)
    
    # add filters 
    stmt = stmt.filter(UserModel.age < 30)
    
    # sort
    stmt = stmt.order_by(asc(UserModel.age))
    
    return paginate(stmt)


add_pagination(app)
```