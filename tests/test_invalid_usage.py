from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from pytest import raises

from fastapi_paginate import add_pagination
from fastapi_paginate.paginator import paginate


def test_params_not_set():
    app = FastAPI()
    client = TestClient(app)

    @app.get("/")
    def route():
        return paginate([])

    with raises(RuntimeError, match="Use params or add_pagination"):
        client.get("/")
