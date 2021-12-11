# pylint: disable=unused-argument,redefined-outer-name,import-outside-toplevel,invalid-name
import json
import pytest
from django.test.client import Client, encode_multipart, BOUNDARY
from auth.models import User, Permission

SUPERUSER_EMAIL = "superuserfortests@mail.com"
SUPERUSER_PASSWORD = "superuserpasswordfortests"
TEST_USER_EMAIL = "test_user@mail.com"
TEST_USER_PASSWORD = "qwerty"


@pytest.fixture
def format_multipart_for_put_request():
    def call_me(data):
        request_data = data.copy()
        request_data["data"] = json.dumps(data["data"])
        return encode_multipart(boundary=BOUNDARY, data=request_data)

    return call_me


@pytest.fixture
def format_multipart_for_post_request():
    def call_me(data):
        request_data = data.copy()
        request_data["data"] = json.dumps(data["data"])
        return request_data

    return call_me


@pytest.fixture
def superuser(db):
    user = User.objects.filter(email=SUPERUSER_EMAIL)
    if user.exists():
        return user.first()

    return User.objects.create_superuser(
        email=SUPERUSER_EMAIL,
        password=SUPERUSER_PASSWORD,
    )


@pytest.fixture
def su_client(superuser):
    response = Client().post(
        "/api/auth/tokens/obtain/",
        {"email": SUPERUSER_EMAIL, "password": SUPERUSER_PASSWORD},
        content_type="application/json",
    )
    access_token = response.data["access"]
    return Client(HTTP_AUTHORIZATION=f"Bearer {access_token}")


@pytest.fixture
def permission_data():
    def call_me(viewset: str = "null", method: str = "get", scope: str = "self"):
        return {
            "viewset": viewset,
            "method": method,
            "scope": getattr(Permission.Scope, scope.upper()),
        }

    return call_me


@pytest.fixture
def test_user(db):
    user = User.objects.filter(email=TEST_USER_EMAIL)
    if user.exists():
        return user.first()

    user = User.objects.create_user(email=TEST_USER_EMAIL, password=TEST_USER_PASSWORD)
    user.save()
    return user


@pytest.fixture
def test_client(test_user):
    response = Client().post(
        "/api/auth/tokens/obtain/",
        {"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD},
        content_type="application/json",
    )
    access_token = response.data["access"]
    return Client(HTTP_AUTHORIZATION=f"Bearer {access_token}")
