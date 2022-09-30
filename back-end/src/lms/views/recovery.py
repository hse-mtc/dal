from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from auth.models import User
from auth.tokens.registration import generate_regconf_token
from common.email.registration import send_change_password_email
from django.contrib.auth.base_user import BaseUserManager


class RecoveryView(generics.GenericAPIView):

    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        email = BaseUserManager.normalize_email(data["email"])

        if not User.objects.filter(email=email).exists():
            return Response(status=status.HTTP_200_OK)

        user = User.objects.get(email=email)

        send_change_password_email(
            email=user.email,
            url=request.META["HTTP_REFERER"],
            token=generate_regconf_token(user),
        )

        return Response(status=status.HTTP_200_OK)
