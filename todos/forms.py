from django import forms
from todos.models import Tasks
from django.contrib.auth.models import User
class TasksForm(forms.ModelForm):
    class Meta:
        model=Tasks
        exclude=('status',)
        widgets={
            "task_name":forms.TextInput(attrs={"class":"form-control"}),
            "user":forms.TextInput(attrs={"class":"form-control"}),
            "date":forms.TextInput(attrs={"class":"form-control"}),
            "status":forms.FileInput(attrs={"class":"form-control"})

        }

class RegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password']

        
class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))