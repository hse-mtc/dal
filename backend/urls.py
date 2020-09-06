from django.urls import path

from backend.views import (
    authors,
    delete_document,
    documents,
    get_file,
    get_tags,
    info,
    login,
    logout,
    published_places,
    subjects,
    CategoryView,
    SubjectSectionView,
    UploadNirView,
)

urlpatterns = [
    path("authors/", authors),
    path("category/", CategoryView.as_view()),
    path("delete_document/", delete_document),
    path("documents/", documents),
    path("get_file/", get_file),
    path("get_tags/", get_tags),
    path("published_places/", published_places),
    path("subject/", SubjectSectionView.as_view()),
    path("subjects/", subjects),
    path("upload/", UploadNirView.as_view()),
    path("user/info/", info),
    path("user/login/", login),
    path("user/logout/", logout),
]
