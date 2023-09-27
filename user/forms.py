from django import forms
from .models import UserProfile, User


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'email']
        

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'name', 'phone_no', 'address', 'email']
