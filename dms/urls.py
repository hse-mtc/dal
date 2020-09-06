from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from backend.views import populate

from mil_lms_backend.views.populate import lms_populate

SchemaView = get_schema_view(
    openapi.Info(
        title="DMS and LMS REST API",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Internal
    path("admin/", admin.site.urls),
    path("populate/", populate),
    path("lms_populate/", lms_populate),

    # Public API
    path("api/", include("backend.urls")),
    path("api/lms/", include("mil_lms_backend.urls")),

    # Swagger
    path("swagger/",
         SchemaView.with_ui("swagger", cache_timeout=0),
         name="schema-swagger-ui"),
]
