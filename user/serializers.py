from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "is_active"]


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
            elif user.password != password_value:
                raise serializers.ValidationError('Invalid credential')
        else:
            raise serializers.ValidationError('Must include "email" and "password".')
        return attrs


class InviteSerializer(serializers.Serializer):
    projectId = serializers.IntegerField(required=True)
    email = serializers.EmailField(required=True)
    role = serializers.IntegerField(required=True)