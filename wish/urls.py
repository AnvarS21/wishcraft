from django.urls import path, include

from rest_framework.routers import DefaultRouter

from wish.views import WishViewSet


router = DefaultRouter()

router.register('', WishViewSet)

urlpatterns = [
    path('', include(router.urls))
]
