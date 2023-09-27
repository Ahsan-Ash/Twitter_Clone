from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import User, UserProfile
import json
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from .forms import UserCreationForm
# Create your views here.

#************************Create User****************************

@csrf_exempt
def create_user(request):
    try:
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                response_data = {
                    "message": f"User {user.username} created successfully.",
                    "User_ID": user.id,
                    "Name": user.name,
                    "Email": user.email,
                }
                return JsonResponse(response_data, status=201)  # 201 Created
            else:
                return HttpResponse("Invalid form data.", status=400)
        elif request.method == "GET":
            form = UserCreationForm()
            return render(request, 'user/create_user_form.html', {'form': form})
        else:
            return HttpResponse("Method Not Allowed", status=405)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

#**************************Get/Retrieve User***********************


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

#**************************Updating User***************************

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

#**************************Delete User***************************

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

        return HttpResponse("User deleted successfully.", status=204)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
    
    
    
#****************************User Profile*************************

@csrf_exempt
def update_user_profile(request):
    if request.method == "POST":
        try:
            user = request.user 
            bio = request.POST.get("bio")
            name = request.POST.get("name")
            phone_no = request.POST.get("phone_no")
            address = request.POST.get("address")
            email = request.POST.get("email")

            if not user:
                return HttpResponse("User not found.", status=404)

            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.bio = bio
            user_profile.name = name
            user_profile.phone_no = phone_no
            user_profile.address = address
            user_profile.email = email
            user_profile.save()

            return JsonResponse({"message": "User profile updated successfully."}, status=200)
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)
    else:
        return HttpResponse("Method Not Allowed", status=405)
    
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