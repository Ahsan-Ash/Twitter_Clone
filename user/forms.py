from django import forms
from django.forms import ModelForm
from .models import UserProfile, User


class UserForm(forms.Form):
    username = forms.CharField(max_length = 12)
    name = forms.CharField(max_length=25)
    email = forms.EmailField()

# class UserProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['bio', 'name', 'phone_no', 'address', 'email']


class UserProfileForm(forms.Form):
    username = forms.CharField(max_length=50)
    bio = forms.CharField()
    name = forms.CharField()
    email = forms.EmailField()
    phone_no = forms.IntegerField()
    address = forms.CharField()


"""class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = "__all__"""