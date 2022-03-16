from rest_framework import serializers
from auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if not (email := attrs.pop("email", None)):
            return super().validate(attrs)

        corporate_email_ending = "@edu.hse.ru"
        if not email.endswith(corporate_email_ending):
            raise serializers.ValidationError(
                f"Corporate email must end with {corporate_email_ending}"
            )
        attrs["email"] = email.lower()
        return super().validate(attrs)

    class Meta:
        model = User
        fields = ["password", "email"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
