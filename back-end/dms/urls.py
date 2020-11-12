from django.urls import path, include

from rest_framework import routers

from dms.views import (
    AuthorViewSet,
    BookViewSet,
    CategoryViewSet,
    ClassMaterialViewSet,
    PaperViewSet,
    PublisherViewSet,
    SectionViewSet,
    SubjectViewSet,
    TagListAPIView,
    TopicViewSet,
)

router = routers.DefaultRouter()
router.register("authors", AuthorViewSet)
router.register("books", BookViewSet)
router.register("categories", CategoryViewSet)
router.register("class-materials", ClassMaterialViewSet)
router.register("papers", PaperViewSet)
router.register("publishers", PublisherViewSet)
router.register("sections", SectionViewSet)
router.register("subjects", SubjectViewSet)
router.register("topics", TopicViewSet)

urlpatterns = [
    # REST router
    path("", include(router.urls)),

    # Manual urls
    path("tags/", TagListAPIView.as_view()),
]
