from django.contrib import admin

from .models import User, Post


@admin.register(User)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('phone', 'access_token')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('token', 'access_token', 'user_phone')

    @admin.display(description='User Phone')
    def user_phone(self, obj):
        if obj.user is None:
            return 'None'
        return obj.user.phone
