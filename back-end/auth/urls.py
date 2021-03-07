from django.urls import path

from auth.views import (info, ProfileRetrieveAPIView,
                        TokenObtainPairExtendedView, TokenRefreshExtendedView,
                        AuthLink)

urlpatterns = [
    path("users/info/", info),
    path("profile/", ProfileRetrieveAPIView.as_view()),
    path("tokens/obtain/", TokenObtainPairExtendedView.as_view()),
    path("tokens/refresh/", TokenRefreshExtendedView.as_view()),
    path("send_access_token/<str:email>/", AuthLink.as_view()),
]
