from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django import forms 
from .models import CustomUser

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address')

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user
    
class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']

class CustomUserChange(UserChangeForm):
    class Meta:
        fields = ['profile_picture', 'bio', 'username']
        model = CustomUser