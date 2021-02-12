from django.urls import path

from auth.views import (
    info,
    ProfileRetrieveAPIView,
)

urlpatterns = [
    path("users/info/", info),
    path("profile/", ProfileRetrieveAPIView.as_view()),
]
