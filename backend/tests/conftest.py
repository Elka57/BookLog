# tests/conftest.py
import pytest
from rest_framework.test import APIClient
from users.models import User, UserTypes
import pytest

from tests.factories import AuthorFactory, UserFactory  # <— OK, 'tests' лежит в корне


@pytest.fixture
def author(db):
    return AuthorFactory()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture(params=[
    UserTypes.READER,
    UserTypes.JOURNALIST,
    UserTypes.STAFF,
    UserTypes.ADMIN,
])
def user_factory(db, django_user_model, request):
    def make_user(**kwargs):
        utype = request.param
        user = django_user_model.objects.create_user(
            username=f"{utype}_{kwargs.get('username', 'test')}",
            password="pass1234",
            user_type=utype
        )
        return user
    return make_user
