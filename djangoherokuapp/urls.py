"""djangoherokuapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from herokuapp.views import login, info, logout, articles, nir, subjects, educational_materials, authors, \
    published_places

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/articles', articles),
    path('api/authors', authors),
    path('api/educational_materials', educational_materials),
    path('api/nir', nir),
    path('api/published_places', published_places),
    path('api/subjects', subjects),
    path('api/user/info', info),
    path('api/user/login', login),
    path('api/user/logout', logout),
]
