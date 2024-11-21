from django.contrib import admin

from friendship.models import Friendship


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'friend', 'status', 'created_at')
