from django.urls import path, include
from rest_framework.routers import DefaultRouter

from auth.views import (
    PermissionRetrieveView,
    RecoveryView,
    UserRetrieveAPIView,
    UserControlViewSet,
    GroupViewSet,
    TokenObtainPairView,
    TokenRefreshView,
    ChangePasswordAPIView,
)

router = DefaultRouter()
# Using routers.register does not register DELETE and POST
# actions properly, so I register them by hand
router.register("user-control", UserControlViewSet)
router.register("group", GroupViewSet)
router.register("permissions", PermissionRetrieveView)

urlpatterns = [
    path(
        "user-control/<int:pk>/transfer-permissions/",
        UserControlViewSet.as_view(
            {
                "patch": "transfer_permissions",
            }
        ),
    ),
    path(
        "user-control/<int:pk>/permissions/all/",
        UserControlViewSet.as_view(
            {
                "delete": "clear_permissions",
            }
        ),
    ),
    path(
        "user-control/<int:pk>/permissions/",
        UserControlViewSet.as_view(
            {"post": "add_permissions", "delete": "delete_permissions"}
        ),
    ),
    path(
        "user-control/<int:pk>/groups/",
        UserControlViewSet.as_view({"post": "add_groups", "delete": "delete_groups"}),
    ),
    path(
        "group/<int:pk>/permissions/",
        GroupViewSet.as_view(
            {"post": "add_permissions", "delete": "delete_permissions"}
        ),
    ),
    path("", include(router.urls)),
    path("user/", UserRetrieveAPIView.as_view()),
    path("tokens/obtain/", TokenObtainPairView.as_view()),
    path("tokens/refresh/", TokenRefreshView.as_view()),
    path("password/change/", ChangePasswordAPIView.as_view()),
    path("recovery/", RecoveryView.as_view()),
]
