from django.urls import path

from rest_framework_simplejwt.views import (
    token_obtain_pair,
    token_refresh,
)

from auth.views import (
    info,
    logout,
)

urlpatterns = [
    path("users/login/", token_obtain_pair),
    path("users/refresh/", token_refresh),
    path("users/info/", info),
    path("user/logout/", logout),
]
