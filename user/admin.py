from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile
from tweet.models import Tweet
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'display_shared_tweets')

    def display_shared_tweets(self, obj):
        shared_tweets = Tweet.objects.filter(share_with=obj)
        return ', '.join([tweet.title for tweet in shared_tweets])
    display_shared_tweets.short_description = 'Shared Tweets'



admin.site.register(User,UserAdmin)
admin.site.register(UserProfile)