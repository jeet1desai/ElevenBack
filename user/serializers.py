from rest_framework import serializers
from .models import User, Company

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "is_active", "country_code", "phone_number", "profile_picture", "address", "gender", "is_superuser"]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email_value = attrs.get("email")
        password_value = attrs.get('password')

        if email_value and password_value:
            try:
                user = User.objects.get(email=email_value, is_active=True)
            except User.DoesNotExist:
                user = None
            if user is None:
                raise serializers.ValidationError('User not found.')
        else:
            raise serializers.ValidationError('Must include "email" and "password".')
        return attrs


class InviteSerializer(serializers.Serializer):
    projectId = serializers.IntegerField(required=True)
    email = serializers.EmailField(required=True)
    role = serializers.IntegerField(required=True)


class UserProfileUpdateSerializer(serializers.Serializer):
    gender = serializers.IntegerField(required=False)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    country_code = serializers.CharField(required=False, allow_blank=True)
    profile_picture = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)


class CompSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "company"]

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"
        extra_kwargs = { 'user': {'required': False} }

    def validate(self, attrs):
        user = self.context.get("user")
        if not User.objects.filter(email=user.email, is_superuser=True).exists():
            raise serializers.ValidationError("User is not authorized to perform this task")
        if Company.objects.filter(user=user).exists():
            raise serializers.ValidationError("Company already exist")
        return attrs
