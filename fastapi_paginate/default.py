from __future__ import annotations

import math
from typing import Generic, Optional, Sequence, TypeVar

from fastapi import Query
from pydantic import BaseModel, conint
from starlette.requests import Request

from .bases import AbstractParams, BasePage, RawParams

T = TypeVar("T")


class Params(BaseModel, AbstractParams):
    page: int = Query(1, ge=1, description="Page number")
    size: int = Query(50, ge=1, le=100, description="Page size")

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.size,
            offset=self.size * (self.page - 1),
        )


class Page(BasePage[T], Generic[T]):
    page: conint(ge=1)  # type: ignore
    size: conint(ge=1)  # type: ignore
    next: Optional[str] = None
    previous: Optional[str] = None
    first: Optional[str] = None
    last: Optional[str] = None
    total: Optional[int] = 0

    __params_type__ = Params

    @classmethod
    def create(cls, items: Sequence[T], total: int, params: AbstractParams, request: Request) -> Page[T]:
        if not isinstance(params, Params):
            raise ValueError("Page should be used with Params")

        next = None
        previous = None
        first = None
        last = None

        last_page = math.ceil(total / params.size)
        prev_page = params.page - 1

        query_params = str(request.query_params)

        previous = (
            f"{request.url.path}?{query_params.replace(f'page={params.page}',f'page={prev_page}')}"
            if prev_page >= 1
            else None
        )

        next = (
            f"{request.url.path}?{query_params.replace(f'page={params.page}',f'page={params.page+1}')}"
            if params.page + 1 <= last_page
            else None
        )

        first = (
            f"{request.url.path}?{query_params.replace(f'page={params.page}',f'page=1')}" if params.page > 1 else None
        )

        last = (
            f"{request.url.path}?{query_params.replace(f'page={params.page}',f'page={last_page}')}"
            if params.page != last_page and last_page > 0
            else None
        )

        return cls(
            total=total,
            items=items,
            page=params.page,
            size=params.size,
            next=next,
            previous=previous,
            first=first,
            last=last,
        )


__all__ = [
    "Params",
    "Page",
]
