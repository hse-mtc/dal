from django.contrib import admin
from django.conf.urls.static import static
from django.urls import (
    include,
    path,
)

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

from conf import settings
from dms.populate import populate as dms_populate
from lms.views.populate import lms_populate
from tgbot.views import populate as tgbot_populate

urlpatterns = [
    # Swagger
    path("swagger/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/",
         SpectacularSwaggerView.as_view(url_name="schema"),
         name="swagger-ui"),

    # Public
    path("api/auth/", include("auth.urls")),
    path("api/dms/", include("dms.urls")),
    path("api/lms/", include("lms.urls")),
    path("api/tgbot/", include("tgbot.urls")),

    # Internal
    path("admin/", admin.site.urls),
    path("populate/dms/", dms_populate),
    path("populate/lms/", lms_populate),
    path("populate/tgbot/", tgbot_populate),
]

# Serve media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
        path("silk/", include("silk.urls", namespace="silk")),
    ]
