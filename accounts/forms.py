# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким Email уже существует")
        return email

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя или Email", max_length=150)

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("avatar", "bio")