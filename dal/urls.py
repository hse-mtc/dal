from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache

from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from dal.settings import DEBUG
from dms.views import populate
from lms.views.populate import lms_populate

index_view = never_cache(TemplateView.as_view(template_name="index.html"))

SchemaView = get_schema_view(
    openapi.Info(
        title="DAL REST API",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Frontend
    path("", index_view, name="index"),

    # Public API
    path("api/", include("dms.urls")),
    path("api/lms/", include("lms.urls")),

    # Swagger
    path("swagger/",
         SchemaView.with_ui("swagger", cache_timeout=0),
         name="schema-swagger-ui"),

    # Internal
    path("admin/", admin.site.urls),
    path("populate/", populate),
    path("lms_populate/", lms_populate),
]

if DEBUG:
    import debug_toolbar
    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
