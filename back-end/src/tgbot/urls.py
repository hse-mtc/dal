from django.urls import path, include

from rest_framework.routers import DefaultRouter

from tgbot.views import SessionViewSet

routers = DefaultRouter()
routers.register("session", SessionViewSet)

urlpatterns = [
    path("", include(routers.urls)),
]
