from django.urls import path

from auth.views import (
    ProfileRetrieveAPIView,
    TokenObtainPairExtendedView,
    TokenRefreshExtendedView,
    CreatePasswordAPIView,
)

urlpatterns = [
    path("profile/", ProfileRetrieveAPIView.as_view()),
    path("tokens/obtain/", TokenObtainPairExtendedView.as_view()),
    path("tokens/refresh/", TokenRefreshExtendedView.as_view()),
    path("password/create/", CreatePasswordAPIView.as_view()),
]
