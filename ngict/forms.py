from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Assessment, Question, Answer, Note
# ... rest of your code ...


class UserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(max_length=1000, required=True)
    password2 = forms.CharField(max_length=1000, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


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