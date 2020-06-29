from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)

from django.test import TestCase, Client
from django.urls import reverse

# import lms_populate
from .views.populate import lms_populate

# import serializers and views
from .serializers import (
    StudentSerializer
)


# initialize the APIClient app
POPULATED = False

client = Client()


class StudentViewTest(TestCase):
    def setUp(self):
        if not POPULATED:
            client.put(reverse('lms_populate'))
    
    def test_get(self):
        response = client.get(reverse('api/lms/student'))
        print(response)