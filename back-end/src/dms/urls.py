from django.urls import (
    path,
    include,
)

from rest_framework import routers

from dms.views.books import (
    BookViewSet,
    FavoriteBookViewSet,
)
from dms.views.papers import (
    PaperViewSet,
    CategoryViewSet,
    TagListAPIView,
)
from dms.views.class_materials import (
    SectionViewSet,
    SectionOrderUpdateAPIView,
    TopicViewSet,
    TopicOrderUpdateAPIView,
    ClassMaterialViewSet,
)
from dms.views.common import (
    AuthorViewSet,
    PublisherViewSet,
    SubjectViewSet,
    StatisticsAPIView,
)

router = routers.DefaultRouter()
router.register("authors", AuthorViewSet)
router.register("books", BookViewSet)
router.register("favorite-books", FavoriteBookViewSet)
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
    # Ordering
    path("sections/<int:id>/order/", SectionOrderUpdateAPIView.as_view()),
    path("topics/<int:id>/order/", TopicOrderUpdateAPIView.as_view()),
    # Statistics
    path("statistics/<int:uid>/", StatisticsAPIView.as_view()),
    # Papers tags
    path("tags/", TagListAPIView.as_view()),
]
