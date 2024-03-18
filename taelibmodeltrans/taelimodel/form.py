from django.contrib.auth.forms import UserCreationForm
from .models import User as u
from django import forms





class userform(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter User Name Here'}))
    email=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Email Here'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Your Password'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Conform Password'}))

    class Meta:
        model=u
        fields=['username','email','password1','password2']
# from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)