from datetime import timedelta

from django.contrib.auth import get_user_model

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from conf.settings import REGCONF_TOKEN_LIFETIME

User = get_user_model()


def generate_regconf_token(
    user: User,
    lifetime: timedelta = REGCONF_TOKEN_LIFETIME,
) -> str:
    token = TokenObtainPairSerializer.get_token(user).access_token
    token.set_exp(lifetime=lifetime)
    return token
