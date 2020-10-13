from django.urls import path, include

from rest_framework import routers

from dms.views import (
    AuthorViewSet,
    BookViewSet,
    CategoryViewSet,
    PaperViewSet,
    PublisherViewSet,
    SubjectViewSet,
    TagListAPIView,
)

router = routers.DefaultRouter()
router.register("authors", AuthorViewSet)
router.register("books", BookViewSet)
router.register("categories", CategoryViewSet)
router.register("papers", PaperViewSet)
router.register("publishers", PublisherViewSet)
router.register("subjects", SubjectViewSet)

urlpatterns = [
    # REST router
    path("", include(router.urls)),

    # Manual urls
    path("tags/", TagListAPIView.as_view()),
]
