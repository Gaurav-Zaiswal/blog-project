from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import (
    CreateView
)

from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/register.html'


class ProfileView(ListView):
    template_name = 'users/profile.html'


