from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from wish.permissions import IsAuthor, IsAuthorOrAdmin
from wish.serializers import WishCreateUpdateSerializer, WishDetailSerializer, WishListSerializer
from wish.models import Wish


class WishViewSet(ModelViewSet):
    queryset = Wish.objects.all()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return WishCreateUpdateSerializer
        elif self.action == 'retrieve':
            return WishDetailSerializer
        return WishListSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ('update', 'partial_update'):
            return [IsAuthor()]
        elif self.action == 'delete':
            return [IsAuthorOrAdmin()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
