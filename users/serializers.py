from rest_framework import serializers

from users.constants import INVALID_CREDENTIALS
from users.models import CustomUser
from users.utils import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    """
    This serializer handles user registration by validating and creating new users.
    """

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'is_admin', 'first_name', 'last_name']

    def validate_password(self, value):
        """
        Validate the provided password against set criteria.
        """
        validate_password(value)
        return value

    def create(self, validated_data):
        """
        Create a new user with the provided validated data.
        """
        return CustomUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """
    This serializer handles user authentication and provides JWT tokens upon successful login.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validate the provided username and password.
        """
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user:
            return user
        raise serializers.ValidationError(INVALID_CREDENTIALS)

    def create(self, validated_data):
        """
         Generate JWT tokens for the authenticated user.
        """
        user = validated_data
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset.
    """
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for resetting a password with a token.
    """
    token = serializers.CharField()
    new_password = serializers.CharField()