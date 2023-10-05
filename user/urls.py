from django.urls import path
from . import views

urlpatterns = [
    path('create_user/', views.create_user, name='create_user'),
    path('retrieve_user/', views.retrieve_user, name='retrieve_user'),
    path('update_user/', views.update_user, name='update_user'),
    path('delete_user/', views.delete_user, name='delete_user'),
    
    #User_Profile
    path('update_user_profile/', views.update_user_profile, name='update_user_profile'),
    path('retrieve_user_profile/', views.retrieve_user_profile, name='retrieve_user_profile'),

    #Form
    path("createForm/",views.createForm,name="createForm"),
    path("user_profile_form/",views.user_profile_form, name="user_profile_form")
    
]