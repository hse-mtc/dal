from django.urls import path, include

from rest_framework.routers import DefaultRouter

from lms.views.viewsets import (StudentViewSet, TeacherViewSet,
                                PunishmentViewSet, EncouragenementViewSet)
from lms.views.reference_book import ReferenceBookView
from lms.views.absence import AbsenceViewSet, AbsenceJournalView

routers = DefaultRouter()
routers.register('student', StudentViewSet)
routers.register('teacher', TeacherViewSet)
routers.register('absence', AbsenceViewSet)
routers.register('punishment', PunishmentViewSet)
routers.register('encouragement', EncouragenementViewSet)

urlpatterns = [
    path('', include(routers.urls)),
    path('absence-journal/', AbsenceJournalView.as_view()),
    path('reference-book/', ReferenceBookView.as_view())
]
