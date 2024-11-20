from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.status import  HTTP_201_CREATED
from rest_framework.views import APIView

from account.models import OTPToken
from account.serializers import UserDetailSerializer, UserRegisterSerializer, OTPTokenSerializer
from core.tasks import send_confirmation_email_task

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
