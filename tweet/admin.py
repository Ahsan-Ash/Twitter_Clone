from django.contrib import admin
from .models import Tweet, Comment
# Register your models here.

class TweetAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_at', 'display_shared_with')

    def display_shared_with(self, obj):
        shared_with_users = obj.share_with.all()
        return ', '.join([user.username for user in shared_with_users])
    display_shared_with.short_description = 'Shared with Users'


admin.site.register(Tweet, TweetAdmin)
admin.site.register(Comment)
