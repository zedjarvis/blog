from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile
from django.utils import timezone


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

        widgets = {
            'username': forms.TextInput(attrs={'type': 'text',
                                               'class': 'form-control'})
        }


def past_years(ago):
    this_year = timezone.now().year
    return list(range(this_year-ago-1, this_year))


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'phone_number',
                  'birth_date', 'profile_image', 'gender']

        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date',
                                                 'class': 'form-control'})
        }
