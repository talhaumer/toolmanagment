from django.urls import path

from user.views import (

    LoginView, AddUserView, EamilVerification, RequestPasswordResetEmail, PasswordTokenCheckAPI, UserLogoutView,
)

urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("signup", AddUserView.as_view(), name="signup"),
    path("email-verification", EamilVerification.as_view(), name="email-verification"),
    path('request-reset-email', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path("logout", UserLogoutView.as_view(), name='user-logout')
]