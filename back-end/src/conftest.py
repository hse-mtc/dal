import json
import pytest
from django.test.client import encode_multipart, BOUNDARY
from auth.models import User

SUPERUSER_EMAIL = "superuserfortests@mail.com"
SUPERUSER_PASSWORD = "superuserpasswordfortests"


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
    from django.test.client import Client
    response = Client().post(
        "/api/auth/tokens/obtain/",
        {
            "email": SUPERUSER_EMAIL,
            "password": SUPERUSER_PASSWORD
        },
        content_type="application/json",
    )
    access_token = response.data["access"]
    return Client(HTTP_AUTHORIZATION=f"Bearer {access_token}")
