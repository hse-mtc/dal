from ams.serializers.register import RegisterSerializer
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from auth.models import User
from auth.tokens.registration import generate_regconf_token
from common.email.registration import send_regconf_email
from django.contrib.sites.shortcuts import get_current_site
import jwt
from django.conf import settings

class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data = user)
        serializer.is_valid(raise_exception = True)
        if User.objects.filter(email = serializer.data['email']).exists():
            pass
        else:
            pass
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email = user_data["email"])
        current_site = get_current_site(request).domain
        send_regconf_email(
            address = user.username,
            email = user.email,
            url = current_site,
            token = generate_regconf_token(user),
        )

        return Response(user_data, status=status.HTTP_201_CREATED)

class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get("token")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id = payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()
        except:
            pass