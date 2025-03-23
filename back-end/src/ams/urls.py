from django.urls import (
    path,
    include,
)

from rest_framework import routers

from ams.views.applicants import ApplicantViewSet
from ams.views.register import RegisterView
from ams.views.military_office import MilitaryOfficeViewSet

router = routers.DefaultRouter()
router.register("applicants", ApplicantViewSet)
router.register(r'military-offices', MilitaryOfficeViewSet)

urlpatterns = [
    # Router.
    path("", include(router.urls)),
    path("register/", RegisterView.as_view(), name="register"),
]
