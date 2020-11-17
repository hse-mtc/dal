from django.urls import path

from auth.views import (
    info,
    ProfileRetrieveAPIView,
    TokenObtainPairExtendedView,
    TokenRefreshExtendedView,
)

urlpatterns = [
    path("users/info/", info),
    path("profile/", ProfileRetrieveAPIView.as_view()),
    path("tokens/obtain/", TokenObtainPairExtendedView.as_view()),
    path("tokens/refresh/", TokenRefreshExtendedView.as_view()),
]
