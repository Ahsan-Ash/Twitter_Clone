from django import forms

class TweetForm(forms.Form):
    user_id = forms.IntegerField()
    title = forms.CharField(max_length=25)
    content = forms.CharField(widget=forms.Textarea)

class TweetShareForm(forms.Form):
    title = forms.CharField(max_length=25)
    # username = forms.CharField()
    user_id =forms.IntegerField()