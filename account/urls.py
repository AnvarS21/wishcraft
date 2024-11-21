from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from account.views import UserView, ActivateAccountView, UserRegisterView, ResetPasswordRequestTokenViewSet, ResetPasswordValidateTokenViewSet, ResetPasswordConfirmViewSet

urlpatterns = [
    path('retrieve/<int:pk>', UserView.as_view()),
    path('activate/', ActivateAccountView.as_view()),
    path('password_reset/', ResetPasswordRequestTokenViewSet.as_view()),
    path('password_reset/validate_token/', ResetPasswordValidateTokenViewSet.as_view()),
    path('password_reset/confirm/', ResetPasswordConfirmViewSet.as_view()),
    path('register/', UserRegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
]
