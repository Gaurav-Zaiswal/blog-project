from django.urls import reverse_lazy
from django.views.generic import View, ListView
from django.views.generic.edit import (
    CreateView
)

from .forms import CustomUserCreationForm
from posts.views import HomeView

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/register.html'


class ProfileView(View):
    '''
    A dashboard for author.

    This view extends HomeView as on dashboard we need listview to list author's posts
    '''

    def get(self, request, *args, **kwargs):
        view = HomeView.as_view(
            template_name='users/profile.html',
            context_object_name='author_posts_list'
        )

        return view(request, *args, **kwargs)

