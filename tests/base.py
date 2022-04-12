from typing import Any, ClassVar, Dict, Type

from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from pydantic import BaseModel
from pytest import fixture, mark

from fastapi_paginate import set_page
from fastapi_paginate.default import Page, Params
from fastapi_paginate.paginator import paginate

from .utils import normalize


class UserOut(BaseModel):
    name: str

    class Config:
        orm_mode = True


_default_params = [
    *[Params(page=i) for i in range(1, 10)],
    *[Params(size=i) for i in range(1, 100, 10)],
    *[Params(page=i, size=j) for i in range(1, 10) for j in range(1, 50, 10)],
]


class BasePaginationTestCase:
    page: ClassVar[Type[Page]] = Page

    @fixture(scope="session")
    def additional_params(self) -> Dict[str, Any]:
        return {}

    @fixture(scope="session")
    def model_cls(self):
        return UserOut

    @mark.parametrize(
        "params,cls_name,path",
        [*[(p, "page", "/default") for p in _default_params]],
    )
    @mark.asyncio
    async def test_pagination(
        self,
        clear_database,
        client,
        params,
        entities,
        cls_name,
        path,
        additional_params,
        model_cls,
    ):
        response = await client.get(path, params={**params.dict(), **additional_params})

        cls = getattr(self, cls_name)
        set_page(cls)

        expected = self._normalize_expected(paginate(entities, params))

        a, b = normalize(
            cls[model_cls],
            self._normalize_model(expected),
            self._normalize_model(response.json()),
        )
        assert a == b

    def _normalize_expected(self, result):
        return result

    def _normalize_model(self, obj):
        return obj

    @fixture(scope="session")
    async def client(self, app):
        async with LifespanManager(app), AsyncClient(app=app, base_url="http://testserver") as c:
            yield c


__all__ = ["BasePaginationTestCase", "UserOut"]
