from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from .models import User, Profile

from tempus_dominus.widgets import DatePicker


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class CustomProfileChangeForm(UserChangeForm):

    class Meta:
        model = Profile
        fields = ('image', 'dob', 'country')

    dob = forms.DateField(widget=DatePicker())
    date_field_required_with_min_max_date = forms.DateField(
        required=False,
        widget=DatePicker(
            options={
                'minDate': '1960-01-01',
                'maxDate': '2005-01-01',
            },
            attrs={
                'input_toggle': False,
                'input_group': False,
            },
        ),
        initial='1993-01-01',
    )
