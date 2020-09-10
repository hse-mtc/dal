from django.urls import path

from dms.views import (
    authors,
    delete_document,
    documents,
    get_file,
    tags,
    info,
    login,
    logout,
    publishers,
    subjects,
    CategoryView,
    SubjectSectionView,
    UploadNirView,
)

urlpatterns = [
    path("authors/", authors),
    path("categories/", CategoryView.as_view()),
    path("delete_document/", delete_document),
    path("documents/", documents),
    path("get_file/", get_file),
    path("tags/", tags),
    path("publishers/", publishers),
    path("subject/", SubjectSectionView.as_view()),
    path("subjects/", subjects),
    path("upload/", UploadNirView.as_view()),
    path("user/info/", info),
    path("user/login/", login),
    path("user/logout/", logout),
]
