from django.contrib import admin
from django.utils.safestring import mark_safe

from wish.models import Wish


@admin.register(Wish)
class WishAdmin(admin.ModelAdmin):
    list_display = ('caption', 'price', 'user', 'get_image')

    def get_image(self, obj):
        return mark_safe(f"<img src='{obj.image.url}' width=100>")
