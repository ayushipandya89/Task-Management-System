from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import path

from users.views import RegisterView, LoginView, PasswordResetRequestView

urlpatterns = [
    path('register', RegisterView.as_view(), name="register_user"),
    path('login', LoginView.as_view(), name='login'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/<uid>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]

