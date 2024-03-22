from django.core.validators import RegexValidator
from rest_framework import serializers

from .models import UserModel


class RegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'login', 'email', 'countryCode', 'isPublic',
                  'password', 'phone', 'image']


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["login", "email", "countryCode", "isPublic", "phone",
                  "image"]


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["countryCode", "isPublic", "phone", "image"]

    def update(self, instance, validated_data):
        instance.countryCode = validated_data.get("countryCode",
                                                  instance.countryCode)
        instance.isPublic = validated_data.get("isPublic", instance.isPublic)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.image = validated_data.get("image", instance.image)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    oldPassword = serializers.CharField()
    newPassword = serializers.CharField(
        max_length=100, validators=[RegexValidator(
            regex=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{6,100}$',
            message="Пароль не удовлетворяет требованиям"
        )])
