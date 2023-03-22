from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.core import exceptions

from myauth.utils import check_recaptcha

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    recaptcha_value = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user

    def validate(self, data):
        if not check_recaptcha({'recaptcha': data.get('recaptcha_value')}):
            raise serializers.ValidationError("Recaptcha required")

        user = UserModel(username=data.get('username'), password=data.get('password'))
        password = data.get('password')

        errors = {}
        try:
            password_validation.validate_password(password=password, user=user)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSerializer, self).validate(data)

    class Meta:
        model = UserModel
        fields = ("id", "username", "password", "recaptcha_value")
