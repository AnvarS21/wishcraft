from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.status import  HTTP_201_CREATED
from rest_framework.views import  APIView
from account.models import OTPToken
from account.serializers import UserDetailSerializer, UserRegisterSerializer, OTPTokenSerializer, \
    PasswordResetSerializer, ValidateOTPTokenSerializer, ResetPasswordSerializer
from core.tasks import send_confirmation_email_task
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
        otp = OTPToken.objects.create(user=user, purpose='registration')
        send_confirmation_email_task.delay(user.email, otp.token)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

class ActivateAccountView(CreateAPIView):
    queryset = OTPToken.objects.all()
    serializer_class = OTPTokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.data.get('token')
        otp = OTPToken.objects.filter(token=token, purpose='registration').first()
        if otp and otp.is_valid():
            user = otp.user
            user.is_active = True
            user.save()
            otp.delete()
            return Response({"message": "Account activated."}, status=200)
        otp.delete()
        return Response({"error": "Invalid or expired token."}, status=400)



class RequestPasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email, is_active=True).first()
            if user:
                otp = OTPToken.objects.create(user=user, purpose='password_reset')
                send_confirmation_email_task.delay(user.email, otp.token)
                return Response({"message": "Password reset token sent to email."}, status=status.HTTP_200_OK)
            return Response({"error": "User not found or inactive."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ValidateOTPTokenView(APIView):
    def post(self, request):
        serializer = ValidateOTPTokenSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            otp = OTPToken.objects.filter(token=token).first()
            if otp.is_valid:
                return Response({"message": "Token is valid"}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successful."}, status=200)

        return Response(serializer.errors, status=400)
