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
# Using routers.register does not register DELETE and POST
# actions properly, so I register them by hand
routers.register("user-control", UserControlViewSet)
routers.register("group", GroupViewSet)

urlpatterns = [
    path(
        "user-control/<int:pk>/permissions/",
        UserControlViewSet.as_view({
            "post": "add_permissions",
            "delete": "delete_permissions"
        })),
    path(
        "user-control/<int:pk>/groups/",
        UserControlViewSet.as_view({
            "post": "add_groups",
            "delete": "delete_groups"
        })),
    path(
        "group/<int:pk>/permissions/",
        GroupViewSet.as_view({
            "post": "add_permissions",
            "delete": "delete_permissions"
        })),
    path("", include(routers.urls)),
    path("user/", UserRetrieveAPIView.as_view()),
    path("tokens/obtain/", TokenObtainPairExtendedView.as_view()),
    path("tokens/refresh/", TokenRefreshExtendedView.as_view()),
    path("password/change/", ChangePasswordAPIView.as_view()),
]
