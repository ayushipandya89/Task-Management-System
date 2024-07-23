from rest_framework import generics, status
from rest_framework.response import Response

from users.constants import USER_CREATED, LOGIN_SUCCESS, NO_USER_FOUND, PASSWORD_RESET_SUCCESSFULLY
from users.permissions import IsNotAuthenticated
from users.serializers import RegisterSerializer, LoginSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from users.serializers import PasswordResetRequestSerializer


# Create your views here.
class RegisterView(generics.CreateAPIView):
    """
    This view allows a user to register by providing a username, email, and password.

    Returns:
        Response: A response with a success message and user data.
    """
    serializer_class = RegisterSerializer
    permission_classes = [IsNotAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"message": USER_CREATED, 'data': serializer.data}, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    """
    This view allows a user to log in by providing a username and password.
    It returns JWT tokens upon successful authentication.

    Returns:
        Response: A response with a success message and JWT tokens.
    """
    serializer_class = LoginSerializer
    permission_classes = [IsNotAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        tokens = serializer.create(user)
        return Response({'message': LOGIN_SUCCESS, 'tokens': tokens}, status=status.HTTP_200_OK)


class PasswordResetRequestView(generics.GenericAPIView):
    """
    View to handle password reset requests.
    """
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": NO_USER_FOUND}, status=status.HTTP_400_BAD_REQUEST)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

        send_mail(
            'Password Reset Request',
            f'Click the link to reset your password: {reset_link}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return Response({"message": PASSWORD_RESET_SUCCESSFULLY}, status=status.HTTP_200_OK)
