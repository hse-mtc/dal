from django.urls import path

from auth.views import (
    UserRetrieveAPIView,
    TokenObtainPairExtendedView,
    TokenRefreshExtendedView,
    CreatePasswordAPIView,
    ChangePasswordAPIView,
)

urlpatterns = [
    path("user/", UserRetrieveAPIView.as_view()),
    path("tokens/obtain/", TokenObtainPairExtendedView.as_view()),
    path("tokens/refresh/", TokenRefreshExtendedView.as_view()),
    path("password/create/", CreatePasswordAPIView.as_view()),
    path("password/change/", ChangePasswordAPIView.as_view()),
]
