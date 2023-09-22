from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import User
import json
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

#****************************************************************
#Create User
@csrf_exempt
def create_user(request):
    try:
        
        username = request.GET.get("username")
        name = request.GET.get("name")
        email = request.GET.get("email")

        if not username or not name or not email:
            return HttpResponse("Missing required data in the request.", status=400)

        user = User.objects.create(username=username, name=name, email=email)

        response_data = {
            "message": f"User {user.username} created successfully.",
            "User_ID": user.id,
            "Name": user.name,
            "Email": user.email,
        }

        return JsonResponse(response_data, status=201)  # 201 Created
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

#****************************************************************
#Get/Retrieve User

def retrieve_user(request):
    try:
        
        username = request.GET.get("username")

        
        if not username:
            return HttpResponse("Username is required.", status=400)

        users = User.objects.filter(username=username)

        if not users.exists():
            return HttpResponse("User not found.", status=404)

        user_data = []
        for user in users:
            user_info = {
                "User_ID": user.id,
                "Name": user.name,
                "Email": user.email,
            }
            user_data.append(user_info)

        return JsonResponse(user_data, safe=False)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

#****************************************************************
#Updating User
@csrf_exempt
def update_user(request):
    try:
        
        user_id = request.GET.get("user_id")
        name = request.GET.get("name")
        email = request.GET.get("email")

        if not user_id:
            return HttpResponse("User ID is required.", status=400)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return HttpResponse("User not found.", status=404)

        if name:
            user.name = name
        if email:
            user.email = email

        user.save()

        response_data = {
            "message": f"User {user.username} updated successfully.",
            "User_ID": user.id,
            "Name": user.name,
            "Email": user.email,
        }

        return JsonResponse(response_data)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

#****************************************************************
#Delete User
@csrf_exempt
def delete_user(request):
    try:

        user_id = request.GET.get("user_id")

        if not user_id:
            return HttpResponse("User ID is required.", status=400)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return HttpResponse("User not found.", status=404)

        user.delete()

        return HttpResponse("User deleted successfully.", status=204)  # 204 No Content
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)