from django.contrib import admin
from django.conf.urls.static import static
from django.urls import (
    include,
    path,
)

from conf import settings

urlpatterns = [
    # Public
    path("api/auth/", include("auth.urls")),
    path("api/dms/", include("dms.urls")),
    path("api/lms/", include("lms.urls")),
    path("api/tgbot/", include("tgbot.urls")),

    # Internal
    path("admin/", admin.site.urls),
]

# Serve media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # Swagger
    from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularSwaggerView,
    )
    urlpatterns += [
        path("swagger/schema/", SpectacularAPIView.as_view(), name="schema"),
        path("swagger/",
             SpectacularSwaggerView.as_view(url_name="schema"),
             name="swagger-ui"),
    ]

    # Debug toolbar
    import debug_toolbar
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]

    # Silk profiler
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
