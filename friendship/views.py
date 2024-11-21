from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from friendship.models import Friendship
from friendship.permissions import IsFriend
from friendship.serializers import FriendshipCreateSerializer, FriendshipUpdateSerializer


class SendFriendRequestView(CreateAPIView):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipCreateSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UpdateFriendshipView(UpdateAPIView):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipUpdateSerializer
    permission_classes = (IsFriend, IsAuthenticated)
