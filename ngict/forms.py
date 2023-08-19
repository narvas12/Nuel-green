from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# ... rest of your code ...


class UserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(max_length=1000, required=True)
    password2 = forms.CharField(max_length=1000, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)
