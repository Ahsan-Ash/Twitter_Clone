from django.urls import path
from . import views

urlpatterns = [
    #Tweets
    
    path('create_tweet/', views.create_tweet, name='create_tweet'),
    path('retrieve_tweet', views.retrieve_tweet, name='retrieve_tweet'),
    path('update_tweet/', views.update_tweet, name='update_tweet'),
    path('delete_tweet/', views.delete_tweet, name='delete_tweet'),

    path('retrieve_tweets_with_filters/', views.retrieve_tweets_with_filters, name='retrieve_tweets_with_filters'),

    #Comments
    path('create_comment/', views.create_comment, name='create_comment'),
    path('retrieve_comments/', views.retrieve_comments, name='retrieve_comments'),
]
