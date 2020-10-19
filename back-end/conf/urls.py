from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework import permissions

from drf_yasg2 import openapi
from drf_yasg2.views import get_schema_view

from conf import settings
from dms.populate import populate as dms_populate
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
    path("api/auth/", include("auth.urls")),
    path("api/dms/", include("dms.urls")),
    path("api/lms/", include("lms.urls")),

    # Internal
    path("admin/", admin.site.urls),
    path("dms_populate/", dms_populate),
    path("lms_populate/", lms_populate),
]

# Serve media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
        path("silk/", include("silk.urls", namespace="silk")),
    ]
