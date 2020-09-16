from django.urls import path, include

from rest_framework import routers

from dms.views import (
    AuthorViewSet,
    CategoryViewSet,
    DocumentViewSet,
    PublisherViewSet,
    SubjectSectionView,
    SubjectViewSet,
    get_file,
    info,
    login,
    logout,
    tags,
)

router = routers.DefaultRouter()
router.register(r"authors", AuthorViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"publishers", PublisherViewSet)
router.register(r"subjects", SubjectViewSet)
router.register(r"documents", DocumentViewSet)

urlpatterns = [
    # REST router
    path("", include(router.urls)),

    # Manual urls
    path("get_file/", get_file),
    path("subject/", SubjectSectionView.as_view()),
    path("tags/", tags),
    path("user/info/", info),
    path("user/login/", login),
    path("user/logout/", logout),
]
