from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm as DefaultPasswordChangeForm
from .models import *

class SignUpForm(UserCreationForm):   

    class Meta:
        model = User
        fields = ('username', 'email', 'password1')
        
class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags', 'category', 'image']

class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['email'] = self.instance.user.email
        for field_name in self.fields:
            field = self.fields[field_name]
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Author
        fields = ['email', 'profile_picture', 'description', 'facebook', 'twitter', 'instagram', 'youtube']


class PasswordChangeForm(DefaultPasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            field.widget.attrs.update({'class': 'form-control'})

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']
