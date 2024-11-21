from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.status import  HTTP_201_CREATED
from rest_framework.generics import GenericAPIView
from account.models import OTPToken
from account.serializers import UserDetailSerializer, UserRegisterSerializer, OTPTokenSerializer, \
    PasswordResetSerializer, ResetPasswordSerializer
from rest_framework import status

User = get_user_model()


class UserView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        OTPToken.objects.create(user=user, purpose='registration')
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


class ActivateAccountView(GenericAPIView):
    queryset = OTPToken.objects.all()
    serializer_class = OTPTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.data.get('token')
        otp = OTPToken.objects.filter(token=token, purpose='registration').first()
        if otp:
            if otp.is_valid():
                user = otp.user
                user.is_active = True
                user.save()
                otp.delete()
                return Response({"message": "Account activated."}, status=200)
            otp.delete()
        return Response({"error": "Invalid or expired token."}, status=400)


class ResetPasswordRequestTokenViewSet(GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        user = User.objects.filter(email=email, is_active=True).first()
        if user:
            OTPToken.objects.create(user=user, purpose='password_reset')
            return Response({"message": "Password reset token sent to email."}, status=status.HTTP_200_OK)
        return Response({"error": "User not found or inactive."}, status=status.HTTP_404_NOT_FOUND)


class ResetPasswordValidateTokenViewSet(GenericAPIView):
    serializer_class = OTPTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data.get('token')
        otp = OTPToken.objects.filter(token=token).first()
        if otp:
            if otp.is_valid:
                return Response({"message": "Token is valid"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid or expired token."}, status=status.HTTP_404_NOT_FOUND)


class ResetPasswordConfirmViewSet(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password reset successful."}, status=200)
