# coding=utf-8

from django.contrib import admin
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
    populate,
    published_places,
    subjects,

    CategoryView,
    SubjectSectionView,
    UploadNirView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("populate/", populate),

    path("api/authors", authors),
    path("api/category", CategoryView.as_view()),
    path("api/delete_document", delete_document),
    path("api/documents", documents),
    path("api/get_file", get_file),
    path("api/get_tags", get_tags),
    path("api/published_places", published_places),
    path("api/subject", SubjectSectionView.as_view()),
    path("api/subjects", subjects),
    path("api/upload", UploadNirView.as_view()),
    path("api/user/info", info),
    path("api/user/login", login),
    path("api/user/logout", logout),
]
