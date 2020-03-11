# coding=utf-8

from django.contrib import admin
from django.urls import path

from backend.views import (
    authors,
    delete_document,
    documents,
    fill_with_mock,
    get_file,
    get_tags,
    info,
    login,
    logout,
    published_places,
    subjects,
    XEP,

    SubjectSectionView,
    UploadNirView,
    CategoryView)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("fill_with_mock", fill_with_mock),

    path("api/authors", authors),
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
    path("api/category", CategoryView.as_view()),
    path("api/XEP", XEP),
]
