from django.urls import path, include

from rest_framework import routers

from dms import views
from dms.views import (
    delete_document,
    documents,
    get_file,
    tags,
    info,
    login,
    logout,
    SubjectSectionView,
    UploadNirView,
)

router = routers.DefaultRouter()
router.register(r"authors", views.AuthorViewSet)
router.register(r"categories", views.CategoryViewSet)
router.register(r"publishers", views.PublisherViewSet)
router.register(r"subjects", views.SubjectViewSet)

urlpatterns = [
    # REST router
    path("", include(router.urls)),

    # Manual urls
    path("delete_document/", delete_document),
    path("documents/", documents),
    path("get_file/", get_file),
    path("subject/", SubjectSectionView.as_view()),
    path("tags/", tags),
    path("upload/", UploadNirView.as_view()),
    path("user/info/", info),
    path("user/login/", login),
    path("user/logout/", logout),
]
