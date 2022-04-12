import os
import sqlite3

from django import setup
from django.conf import settings
from django.db import models
from fastapi import FastAPI
from pytest import fixture

from fastapi_paginate import Page, add_pagination
from fastapi_paginate.ext.django import paginate

from ..base import BasePaginationTestCase
from ..utils import faker

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "True"


@fixture(scope="session")
def database_url(sqlite_url) -> str:
    *_, dbname = sqlite_url.split("/")
    return dbname


@fixture(scope="session")
def db(database_url):
    settings.configure(
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": database_url,
            }
        },
        INSTALLED_APPS=[],
    )
    setup()

    sqlite3.connect(database_url)


@fixture(scope="session")
def User(db):
    class User(models.Model):
        id = models.IntegerField(primary_key=True)
        name = models.TextField()

        class Meta:
            app_label = "test"
            db_table = "users"

    return User


@fixture(
    scope="session",
    params=[True, False],
    ids=["model", "query"],
)
def query(request, User):
    if request.param:
        return User
    else:
        return User.objects.all()


@fixture(scope="session")
def app(db, User, query, model_cls):
    app = FastAPI()

    @app.get("/default", response_model=Page[model_cls])
    def route():
        return paginate(query)

    return add_pagination(app)


class TestDjango(BasePaginationTestCase):
    @fixture(scope="class")
    def entities(self, User, query):
        User.objects.bulk_create(User(name=faker.name()) for _ in range(100))

        return [*User.objects.all()]
