from django.urls import path, include
from rest_framework.routers import DefaultRouter

from auth.views import (
    UserRetrieveAPIView,
    UserControlViewSet,
    GroupViewSet,
    TokenObtainPairExtendedView,
    TokenRefreshExtendedView,
    ChangePasswordAPIView,
)

routers = DefaultRouter()
routers.register("user/control", UserControlViewSet)
routers.register("groups", GroupViewSet)

urlpatterns = [
    path("", include(routers.urls)),
    path("user/", UserRetrieveAPIView.as_view()),
    path("tokens/obtain/", TokenObtainPairExtendedView.as_view()),
    path("tokens/refresh/", TokenRefreshExtendedView.as_view()),
    path("password/change/", ChangePasswordAPIView.as_view()),
]
