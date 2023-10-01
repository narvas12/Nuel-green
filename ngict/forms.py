from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from instructors.models import Answer, Assessment, Question
from .models import Note
# ... rest of your code ...





class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(max_length=1000, required=True)
    password2 = forms.CharField(max_length=1000, required=True)

    class Meta:
        # You can add additional fields and options here
        labels = {
            'username': 'Your Username',
            'email': 'Your Email',
            'password1': 'Your Password',
            'password2': 'Confirm Password',
        }
        help_texts = {
            'username': 'Enter a unique username.',
            'email': 'Enter a valid email address.',
            'password1': 'Choose a strong password.',
            'password2': 'Enter the same password as above.',
        }


class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        # You can add additional fields and options here
        labels = {
            'username': 'Your Username',
            'password': 'Your Password',
        }
        help_texts = {
            'username': 'Enter your username.',
            'password': 'Enter your password.',
        }



class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['title', 'description']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']



class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('content',)