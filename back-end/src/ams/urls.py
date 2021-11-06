from django.urls import (
    path,
    include,
)

from rest_framework import routers

from ams.views.applicants import ApplicantViewSet

router = routers.DefaultRouter()
router.register("applicants", ApplicantViewSet)

urlpatterns = [
    # Router.
    path("", include(router.urls)),
]
