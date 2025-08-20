from django import forms
from django.contrib.auth.models import User
from .models import Book, Student

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class StudentForm(forms.ModelForm):
    username = forms.CharField(max_length=150)   # Django username
    password = forms.CharField(widget=forms.PasswordInput)  # Django password

    class Meta:
        model = Student
        fields = ["username", "password", "roll_number", "course"]

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "available"]
