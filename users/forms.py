from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from django import forms

class CustomClearableFileInput(forms.ClearableFileInput):
    template_name = 'users/custom_clearable_file_input.html'

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже зарегистрирован.')
        return email


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']
        widgets = {
            'avatar': CustomClearableFileInput,
        }





