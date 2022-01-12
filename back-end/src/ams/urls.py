from django.urls import (
    path,
    include,
)

from rest_framework import routers

from ams.views.applicants import ApplicantViewSet
from ams.views.register import RegisterView

router = routers.DefaultRouter()
router.register("applicants", ApplicantViewSet)

urlpatterns = [
    # Router.
    path("", include(router.urls)),
    path("register/", RegisterView.as_view(), name="register"),
]
