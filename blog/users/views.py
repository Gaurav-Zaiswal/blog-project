from django.urls import reverse_lazy
from django.views.generic import View, ListView
from django.views.generic.edit import (
    CreateView
)
from django.db.models import Q

from .forms import CustomUserCreationForm
from django.views.generic import ListView
from posts.views import HomeView
from posts.models import Post


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/register.html'


class ProfileView(ListView):
    model = Post
    template_name = "users/profile.html"
    context_object_name = 'author_posts_list'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        # print(self.request.user)
        context['author_all_posts_list'] = Post.objects.filter(author=self.request.user).order_by('-created_on')
        context['author_draft_posts_list'] = Post.objects.filter(
            Q(author=self.request.user) & Q(status=0)).order_by('-created_on')
        return context
