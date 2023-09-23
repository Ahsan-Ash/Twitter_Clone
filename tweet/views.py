from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Tweet
from user.models import User
import json
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

#Creating TWEET
@csrf_exempt
def create_tweet(request):
    if request.method == "POST":
        try:
            user_id = request.GET.get("user_id")
            title = request.GET.get("title")
            content = request.GET.get("content")
            # data = json.loads(request.body.decode('utf-8'))
            # user_id = data.get("user_id")
            # title = data.get("title")
            # content = data.get("content")
            
            if not user_id or not title or not content:
                return HttpResponse("Missing required data in the request.", status=400)

            try:
                user = User.objects.get(id=user_id)
            except ObjectDoesNotExist:
                return HttpResponse("User does not exist.", status=404)

            tweet = Tweet.objects.create(user=user, title=title, content=content)

            response = {
                "message": f"The tweet by {user.username} was created successfully.",
                "Tweet_title": tweet.title,
                "Tweet_content": tweet.content
            }

            return JsonResponse(response, status=201)
        
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)

    else:
        return HttpResponse("Method Not Allowed", status=405)

#****************************************************************
#Getting/Reteriving TWEET
def retrieve_tweet(request):
    try:
        
        user_id = request.GET.get("user_id")
        tweet_id = request.GET.get("tweet_id")

        queryset = Tweet.objects.all()

        if user_id:
            queryset = queryset.filter(user_id=user_id)

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
            
            if not tweet_id:
                return HttpResponse("Tweet ID is required.", status=400)
                
            try:
                tweet = Tweet.objects.get(id=tweet_id)
            except ObjectDoesNotExist:
                return HttpResponse("Tweet not found.", status=404)
                
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

        if not tweet_id:
            return HttpResponse("Tweet ID is required.", status=400)

        try:
            tweet = Tweet.objects.get(id=tweet_id)
        except ObjectDoesNotExist:
            return HttpResponse("Tweet not found.", status=404)

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