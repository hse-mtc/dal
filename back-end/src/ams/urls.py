from django.urls import (
    path,
    include,
)

from rest_framework import routers


router = routers.DefaultRouter()

urlpatterns = [
    # Router.
    path("", include(router.urls)),

]
