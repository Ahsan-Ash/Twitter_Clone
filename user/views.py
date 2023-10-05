from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import User, UserProfile
import json
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from .forms import UserForm, UserProfileForm
from django.contrib.auth import get_user_model

# Create your views here.

#************************Create User****************************

@csrf_exempt
def create_user(request):
    try:
        if request.method == "POST":
            
            username = request.GET.get("username")
            email = request.GET.get("email")
            password = request.GET.get("password")

            User = get_user_model()
            user = User.objects.create_user(username=username, email=email, password=password)
            response_data = {
                "message": f"User {user.username} created successfully.",
                "User_ID": user.id,
                "Name": user.name,
                "Email": user.email,                
            }
            return JsonResponse(response_data, status=201)  # 201 Created
        else:
            return HttpResponse("Invalid form data.", status=400)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

#**************************Get/Retrieve User***********************


def retrieve_user(request):
    try:
        
        username = request.GET.get("username")
        users = User.objects.filter(username=username)

        user_data = []
        for user in users:
            user_info = {
                "User_ID": user.id,
                "Username": user.username,
                "Email": user.email,
            }
            user_data.append(user_info)

        return JsonResponse(user_data, safe=False)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

#**************************Updating User***************************

@csrf_exempt
def update_user(request):
    try:
        
        user_id = request.GET.get("user_id")
        name = request.GET.get("name")
        email = request.GET.get("email")

        user = User.objects.get(id=user_id)

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

#**************************Delete User***************************

@csrf_exempt
def delete_user(request):
    try:

        user_id = request.GET.get("user_id")

        if not user_id:
            return JsonResponse({"error": "User ID is required."}, status=400)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)

        user.delete()

        return JsonResponse({"error": "User deleted successfully."}, status=204)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
    
    
    
#****************************User Profile*************************

@csrf_exempt
def update_user_profile(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))

            user_id = data["user_id"]
            bio = data["bio"]
            name = data["name"]
            phone_no = data["phone_no"]
            address = data["address"]
            email = data["email"]

            user = get_object_or_404(User, id=user_id)
        
            create_user_profile = UserProfile.objects.create(user=user, bio=bio, name=name, phone_no=phone_no, address=address, email=email)
            create_user_profile.save()

            return JsonResponse({"message": "User profile created successfully."}, status=200)
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)
    else:
        return HttpResponse("Method Not Allowed", status=405)
    
#Get UserProfile
    
def retrieve_user_profile(request):
    username = request.GET.get("username")
    if not username:
        return HttpResponse("Username is required.", status=400)

    user_profile = get_object_or_404(UserProfile, user__username=username)

    response_data = {
        "User_ID": user_profile.user.id,
        "Name": user_profile.name,
        "Email": user_profile.email,
        "Bio": user_profile.bio,
        "Phone_No": user_profile.phone_no,
        "Address": user_profile.address,
    }

    return JsonResponse(response_data, status=200)

#****************************Create User Form*************************


def createForm(request):
    if request.method == "GET":
        form = UserForm()
        return render(request,"user/create_user.html",{"form":form})

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            
            new_user = User(username=username , name=name, email=email )
            new_user.save()
            return HttpResponse(f"{username}, User created successfully!")
        else:    
            return render(request,"user/create_user.html",{"form":form})
        
#****************************cREATE User Profile through Form*************************
def user_profile_form(request):
    if request.method == "GET":
        form = UserProfileForm()
        return render(request,"user/userprofile.html",{"form":form})

    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            bio = form.cleaned_data["bio"]
            name = form.cleaned_data["name"]
            phone_no = form.cleaned_data["phone_no"]
            address = form.cleaned_data["address"]
            email = form.cleaned_data["email"]
            
            user = User.objects.get(username=username)

            create_user_profile = UserProfile(user=user, bio=bio, name=name, phone_no=phone_no, address=address, email=email)
            create_user_profile.save()
            return HttpResponse(f" User Profile updated successfully!")
        else:    
            return render(request,"user/userprofile.html",{"form":form})