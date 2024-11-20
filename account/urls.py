from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from account.views import UserView, ActivateAccountView, UserRegisterView

urlpatterns = [
    path('retrieve/<int:pk>', UserView.as_view()),
    path('activate/', ActivateAccountView.as_view()),
    path('register/', UserRegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
]
