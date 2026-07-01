from django.urls import (
    include,
    path,
)
from rest_framework import routers

from ams.views.applicants import ApplicantViewSet
from ams.views.physical import ExerciseListView, ExerciseResultViewSet
from ams.views.register import RegisterView

router = routers.DefaultRouter()
router.register("applicants", ApplicantViewSet)

exercise_results_list = ExerciseResultViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)
exercise_results_detail = ExerciseResultViewSet.as_view(
    {
        "get": "retrieve",
        "patch": "partial_update",
        "put": "update",
        "delete": "destroy",
    }
)
exercise_results_override = ExerciseResultViewSet.as_view(
    {
        "post": "override",
    }
)

urlpatterns = [
    # Router.
    path("", include(router.urls)),
    path("register/", RegisterView.as_view(), name="register"),
    # Physical exercises catalog.
    path(
        "physical/exercises/",
        ExerciseListView.as_view(),
        name="exercise-list",
    ),
    # Exercise results per applicant.
    path(
        "applicants/<int:applicant_pk>/exercise-results/",
        exercise_results_list,
        name="exercise-results-list",
    ),
    # Ручная (дословная) загрузка результатов комиссии — до detail-роута,
    # чтобы "override" не был распознан как exercise_type.
    path(
        "applicants/<int:applicant_pk>/exercise-results/override/",
        exercise_results_override,
        name="exercise-results-override",
    ),
    path(
        "applicants/<int:applicant_pk>/exercise-results/<str:exercise_type>/",
        exercise_results_detail,
        name="exercise-results-detail",
    ),
]
