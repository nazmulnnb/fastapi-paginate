from typing import Generic, Sequence, TypeVar

from pytest import mark, raises

from fastapi_paginate import Page
from fastapi_paginate.bases import AbstractParams, RawParams

T = TypeVar("T")
C = TypeVar("C")


def test_custom_page_invalid_params_cls():
    class CustomParams(AbstractParams):
        def to_raw_params(self) -> RawParams:
            return RawParams(0, 0)

    class CustomPage(Page[T], Generic[T]):
        __params_type__ = CustomParams

    with raises(ValueError, match="^CustomParams must be subclass of BaseModel$"):
        CustomPage.with_custom_options(size=10)


def test_custom_page_invalid_values():
    with raises(ValueError, match="^Unknown field smth_wrong$"):
        Page.with_custom_options(smth_wrong=100)

    with raises(ValueError, match="^Unknown fields a, b, c"):
        Page.with_custom_options(a=1, b=2, c=3)


class MultipleParamsPage(Page[T], Generic[T, C]):
    sub_items: Sequence[C]


@mark.parametrize(
    "cls",
    [Page, Page[int], MultipleParamsPage],
    ids=["non-concrete", "concrete", "non-concrete-multiple-params"],
)
def test_custom_page(cls):
    page_cls = cls.with_custom_options()
    assert page_cls.__params_type__().dict() == {"size": 50, "page": 1}

    page_cls = cls.with_custom_options(size=100)
    assert page_cls.__params_type__().dict() == {"size": 100, "page": 1}

    page_cls = cls.with_custom_options(size=100, page=100)
    assert page_cls.__params_type__().dict() == {"size": 100, "page": 100}
