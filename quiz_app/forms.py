from django import forms
from .models import Question, Answer
from .models import Quiz
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['name', 'description']

class QuestionForm(forms.ModelForm):
    answer1 = forms.CharField(max_length= 100)
    correct1 = forms.BooleanField(required=False)
    answer2 = forms.CharField(max_length= 100)
    correct2 = forms.BooleanField(required=False)
    answer3 = forms.CharField(max_length= 100)
    correct3 = forms.BooleanField(required=False)
    answer4 = forms.CharField(max_length= 100)
    correct4 = forms.BooleanField(required=False)

    class Meta:
        model = Question
        fields = ['quiz', 'question_text']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct', 'question']
