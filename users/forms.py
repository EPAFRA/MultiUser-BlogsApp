from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove help text for each field
        for field in self.fields.values():
            field.help_text = ''

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove help text for each field
        for field in self.fields.values():
            field.help_text = ''

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['gender','image']

   