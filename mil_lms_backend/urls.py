from django.urls import path
from .views import views

urlpatterns = [
    path('student/', views.StudentView.as_view()),
]