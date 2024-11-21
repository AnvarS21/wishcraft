from rest_framework import serializers

from account.serializers import UserDetailSerializer
from wish.models import Wish

class WishCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wish
        fields = ('id', 'name', 'image', 'caption', 'link', 'price', 'user')
        read_only_fields = ('user',)


class WishDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Wish
        fields = ('id', 'user', 'image', 'caption')


class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wish
        fields = ('id', 'image', 'price', 'name')
