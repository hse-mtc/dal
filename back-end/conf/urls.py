from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from conf import settings
from dms.views import populate
from lms.views.populate import lms_populate

SchemaView = get_schema_view(
    openapi.Info(
        title="DAL REST API",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Swagger
    path("",
         SchemaView.with_ui("swagger", cache_timeout=0),
         name="schema-swagger-ui"),

    # Public API
    path("api/", include("dms.urls")),
    path("api/lms/", include("lms.urls")),

    # Internal
    path("admin/", admin.site.urls),
    path("populate/", populate),
    path("lms_populate/", lms_populate),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
