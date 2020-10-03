from django.urls import path, include

from rest_framework import routers

from dms.views import (
    AuthorViewSet,
    CategoryViewSet,
    DocumentViewSet,
    PublisherViewSet,
    SubjectSectionView,
    SubjectViewSet,
    TagListAPIView,
)

router = routers.DefaultRouter()
router.register("authors", AuthorViewSet)
router.register("categories", CategoryViewSet)
router.register("documents", DocumentViewSet)
router.register("publishers", PublisherViewSet)
router.register("subjects", SubjectViewSet)

urlpatterns = [
    # REST router
    path("", include(router.urls)),

    # Manual urls
    path("subject/", SubjectSectionView.as_view()),
    path("tags/", TagListAPIView.as_view()),
]
