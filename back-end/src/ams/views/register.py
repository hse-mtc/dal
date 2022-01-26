from ams.serializers.register import RegisterSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from auth.models import User, Group
from auth.tokens.registration import generate_regconf_token
from common.email.registration import send_regconf_email
from django.contrib.auth.base_user import BaseUserManager


class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        user = request.data
        email = BaseUserManager.normalize_email(user["email"])
        if not email.endswith("@edu.hse.ru"):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not User.objects.filter(email=email).exists():
            user["password"] = User.objects.make_random_password()
            serializer = self.serializer_class(data=user)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        user = User.objects.get(email=email)
        applicants, _ = Group.objects.get_or_create(name="Абитуриет")
        applicants.user_set.add(user)
        send_regconf_email(
            address=user.username,
            email=user.email,
            url=request.META["HTTP_REFERER"],
            token=generate_regconf_token(user),
        )

        return Response(status=status.HTTP_201_CREATED)
