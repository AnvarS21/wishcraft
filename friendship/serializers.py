from rest_framework import serializers

from django.db.models import Q

from friendship.choices import FriendshipStatusChoices
from friendship.models import Friendship


class FriendshipCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Friendship
        fields = ('user', 'friend')
        read_only_fields = ('user',)

    def validate(self, data):
        user = self.context.get('request').user
        friend = data.get('friend')

        if user == friend:
            raise serializers.ValidationError("You cannot send a friend request to yourself.")

        if Friendship.objects.filter(
                Q(user=user, friend=friend) | Q(user=friend, friend=user),
                Q(status=FriendshipStatusChoices.ACCEPTED) | Q(status=FriendshipStatusChoices.PENDING)
        ).exists():
            raise serializers.ValidationError("Friend request already exists between these users.")

        return data


class FriendshipUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ('status', 'friend')
        read_only_fields = ('friend',)