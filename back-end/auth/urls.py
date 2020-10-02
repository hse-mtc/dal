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
    path("users/info/", info),
    path("users/logout/", logout),
    path("tokens/obtain/", token_obtain_pair),
    path("tokens/refresh/", token_refresh),
]

