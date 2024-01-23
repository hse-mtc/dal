from rest_framework import serializers

from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_writable_nested.mixins import UniqueFieldsMixin

from drf_extra_fields.fields import Base64ImageField

from common.models.personal import (
    BirthInfo,
    ContactInfo,
    Passport,
    PersonalDocumentsInfo,
    Photo,
    Relative,
)


def check_email_exists(corporate_email: str):
    return ContactInfo.objects.filter(corporate_email=corporate_email).exists()


class BirthInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BirthInfo
        exclude = ["id"]


class ContactInfoSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        if "corporate_email" not in validated_data:
            return super().create(validated_data)

        corporate_email = validated_data.pop("corporate_email")

        try:
            contact_info = ContactInfo.objects.exclude(
                corporate_email__isnull=True
            ).get(corporate_email=corporate_email)
            result = self.update(contact_info, validated_data)
            validated_data["corporate_email"] = corporate_email
            return result

        except ContactInfo.DoesNotExist:
            validated_data["corporate_email"] = corporate_email
            return super().create(validated_data)

    def update(self, instance, validated_data):
        old_partial = self.partial
        self.partial = True
        result = super().update(instance, validated_data)
        self.partial = old_partial
        return result

    def validate(self, attrs):
        if not (number := attrs.pop("personal_phone_number", None)):
            return super().validate(attrs)

        number: str = number.strip()

        if not number:
            return super().validate(attrs)

        if number.startswith("+"):
            number = number[1:]

        example = "79098080022"

        correct_len = len(number) == len(example)
        if not correct_len:
            raise serializers.ValidationError(
                f"Personal phone number must consist of {len(example)} symbols"
            )

        if number.startswith("8"):
            number = example[0] + number[1:]

        correct_first_symbol = number[0] == example[0]
        if not correct_first_symbol:
            raise serializers.ValidationError(
                f"Personal phone number must start with `{example[0]}`"
            )

        attrs["personal_phone_number"] = number
        return super().validate(attrs)

    class Meta:
        model = ContactInfo
        exclude = ["id"]
        extra_kwargs = {"corporate_email": {"validators": []}}


class PhotoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        use_url=False,
        allow_null=True,
        required=False,
        read_only=True,
    )

    class Meta:
        model = Photo
        exclude = ["id"]


class PhotoMutateMixin(serializers.Serializer):
    image = Base64ImageField(write_only=True, required=False)

    def create_photo(self, validated_data):
        image = validated_data.pop("image", None)
        if image is None:
            return

        photo = Photo.objects.create(image=image)
        validated_data["photo"] = photo

    def update_photo(self, instance, validated_data):
        if "image" not in validated_data:
            return

        if instance.photo:
            instance.photo.delete()

        self.create_photo(validated_data)


class PassportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passport
        exclude = ["id"]


class PersonalDocumentsInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalDocumentsInfo
        exclude = ["id"]


class RelativeSerializer(serializers.ModelSerializer):
    birth_info = BirthInfoSerializer(read_only=True)
    contact_info = ContactInfoSerializer(read_only=True)

    class Meta:
        model = Relative
        exclude = ["id"]


class RelativeMutateSerializer(WritableNestedModelSerializer):
    birth_info = BirthInfoSerializer()
    contact_info = ContactInfoSerializer()

    class Meta:
        model = Relative
        exclude = ["id"]
