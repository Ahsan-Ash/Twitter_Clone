from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Tweet, Comment
from user.models import User
import json
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from .forms import TweetForm, TweetShareForm

# Create your views here.

#Creating TWEET

@csrf_exempt
def create_tweet(request):
    try:
        user_id = request.GET.get('user_id')
        title = request.GET.get('title')
        content = request.GET.get('content')

        user = User.objects.get(id=user_id)
        
        new_tweet = Tweet(title=title, content=content, user=user)
        new_tweet.save()

        response = {
            "message": "Tweet created",
        }
        return JsonResponse(response)
    except json.JSONDecodeError as e:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
#****************************************************************
#Getting/Reteriving TWEET
def retrieve_tweet(request):
    try:
        user_id = request.GET.get("user_id")
        tweet_id = request.GET.get("tweet_id")

        queryset = Tweet.objects.all()

        if user_id:
            queryset = queryset.filter(user__id=user_id)
        if tweet_id:
            queryset = queryset.filter(id=tweet_id)

        tweet = queryset.first()

        if tweet:
            response_data = {
                "Tweet_title": tweet.title,
                "Tweet_content": tweet.content,
                "Created_at": tweet.created_at,
                "User": tweet.user.username,
            }
            return JsonResponse(response_data)
        else:
            return HttpResponse("Tweet not found.", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
    
#****************************************************************
#Updating TWEET
@csrf_exempt
def update_tweet(request):
    if request.method == "PUT":
        try:
            tweet_id = request.GET.get("tweet_id")
            title = request.GET.get("title")
            content = request.GET.get("content")
            
            tweet = Tweet.objects.get(id=tweet_id)
                
            if title:
                tweet.title = title
            if content:
                tweet.content = content
                
            tweet.save()
        
            response = {
                "message": "Tweet updated successfully.",
                "Tweet_title": tweet.title,
                "Tweet_content": tweet.content,
            }
            return JsonResponse(response)
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)
    else:
        return HttpResponse("Method Not Allowed", status=405)
    
#****************************************************************
#Deleting TWEET
@csrf_exempt
def delete_tweet(request):
    try:
        tweet_id = request.GET.get("tweet_id")

        tweet = Tweet.objects.get(id=tweet_id)
        tweet.delete()

        return HttpResponse("Tweet deleted successfully.", status=204)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
    
#****************************************************************
#Getting/Reteriving TWEET with Filter
def retrieve_tweets_with_filters(request):
    try:

        title = request.GET.get("title")
        username = request.GET.get("username")

        queryset = Tweet.objects.all()

        if title:
            queryset = queryset.filter(title__icontains=title)
        if username:
            queryset = queryset.filter(user__username=username)

        tweets = queryset.values(
            "id",
            "title",
            "content",
            "created_at",
            "user__username"
        )

        tweet_data = list(tweets)

        return JsonResponse(tweet_data, safe=False)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
    
    
    
    
# Create Comment
@csrf_exempt
def create_comment(request):
    if request.method == "POST":
        try:
            user_id = request.GET.get("user_id")
            tweet_id = request.GET.get("tweet_id")
            content = request.GET.get("content")

            user = User.objects.get(id=user_id)
            tweet = Tweet.objects.get(id=tweet_id)
 
            comment = Comment.objects.create(user=user, tweet=tweet, content=content)

            response = {
                "message": f"Comment by {user.username} on tweet ID {tweet.id} was created successfully.",
                "Comment_content": comment.content,
            }

            return JsonResponse(response, status=201)

        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)

    else:
        return HttpResponse("Method Not Allowed", status=405)

# Retrieve Comments for a Tweet
def retrieve_comments(request):
    try:
        tweet_id = request.GET.get("tweet_id")
        tweet = Tweet.objects.get(id=tweet_id)

        comments = Comment.objects.filter(tweet=tweet)
        comment_data = []

        for comment in comments:
            comment_info = {
                "Comment_content": comment.content,
                "User": comment.user.username,
            }
            comment_data.append(comment_info)

        return JsonResponse(comment_data, safe=False)

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)


def createForm(request):
    if request.method == "GET":
        form = TweetForm()
        return render(request,"tweet/create_tweet.html",{"form":form})

    if request.method == "POST":
        form = TweetForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            user_id = form.cleaned_data['user_id']
            user = User.objects.get(id=user_id)
            new_tweet = Tweet(title=title , content=content, user=user )
            new_tweet.save()
            return HttpResponse(f"{user.username}, Tweet {title} created successfully!")
        else:    
            return render(request,"tweet/create_tweet.html",{"form":form})
        

        
def shareTweet(request):
    if request.method == "GET":
        form = TweetShareForm()
        return render(request,"tweet/tweet_share.html",{"form":form})
    
    if request.method =="POST":
        form = TweetShareForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            user_id = form.cleaned_data['user_id']
            # username = form.cleaned_data['username']

            tweet = Tweet.objects.get(title=title)
            # user = User.objects.get(username=username)
            user = get_object_or_404(User, pk=user_id)
            all_tweets = user.shared_tweets.all()
            if tweet in all_tweets:
                return HttpResponse(f'Tweet {tweet.title}already shared')
            else:
                share = user.shared_tweets.add(tweet)
                return HttpResponse(f"Tweet {tweet.title} shared Successfully.")
        else:    
            return render(request,"tweet/tweet_share.html",{"form":form})
        
        
