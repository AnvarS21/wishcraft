from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from account.models import OTPToken
from friendship.choices import FriendshipStatusChoices
from friendship.models import Friendship

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=20, required=True, write_only=True)
    password2 = serializers.CharField(min_length=8, max_length=20, required=True, write_only=True)

    class Meta:
        model = User
        fields = ( 'username', 'email', 'password', 'password2')

    def validate_password1(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError({'password2': "Passwords didn't match!"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    wish_count = serializers.SerializerMethodField()
    friend_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'avatar', 'first_name', 'last_name', 'wish_count', 'friend_count')

    def get_wish_count(self, obj):
        return obj.wishcrafts.count()


    def get_friend_count(self, obj):

        return Friendship.objects.filter(
            (Q(user=obj) | Q(friend=obj)),
            status=FriendshipStatusChoices.ACCEPTED
        ).count()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'avatar')

class OTPTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPToken
        fields = ('token',)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField()
    password2 = serializers.CharField()

    def validate_password1(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError({'password2': "Passwords didn't match!"})
        return attrs


    def save(self):
        token = self.validated_data['token']
        otp = OTPToken.objects.filter(token=token, purpose='password_reset').first()

        if otp and otp.is_valid():
            user = otp.user
            user.set_password(self.validated_data['password'])
            user.save()
            otp.delete()
            return user
        else:
            raise serializers.ValidationError({"error": "Invalid or expired token."})
