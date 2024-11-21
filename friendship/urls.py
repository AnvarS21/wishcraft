from django.urls import path

from friendship.views import SendFriendRequestView, UpdateFriendshipView

urlpatterns = [
    path('update/<int:pk>', UpdateFriendshipView.as_view()),
    path('send/', SendFriendRequestView.as_view()),
]
