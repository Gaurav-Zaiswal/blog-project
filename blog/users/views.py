from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import View, ListView
from django.views.generic.edit import (
    CreateView, UpdateView
)
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin

from .forms import CustomProfileChangeForm, CustomUserChangeForm, CustomUserCreationForm
from .models import User, Profile
from posts.views import HomeView
from posts.models import Post
from movies.models import MovieRating


@login_required
def user(request):
    """
    This will return url containing username of logged in user, where user after
    successful login will be redirected.
    """
    url = ('/author/%s/' % request.user.username)
    return HttpResponseRedirect(url)


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/register.html'


@method_decorator(login_required(login_url='/login'), name='dispatch')
class ProfileView(ListView):
    model = Post
    template_name = "users/profile.html"
    context_object_name = 'author_posts_list'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['author_all_posts_list'] = Post.objects.filter(author=self.request.user.id).order_by('-created_on')
        context['author_draft_posts_list'] = Post.objects.filter(
            Q(author=self.request.user.id) & Q(status=0)).order_by('-created_on')
        context['movie_review_list'] = MovieRating.objects.filter(
            author=self.request.user.id
        ).order_by('-created_on')
        return context

@method_decorator(login_required(login_url='/login'), name='dispatch')
class UserUpdateView(SuccessMessageMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = "users/update_user.html"
    success_url = reverse_lazy('users:profile')
    success_message = 'Profile has been updated SuccessFully!'

    def get_queryset(self):
        """ Limit a User to only modifying their own data. """
        qs = super(UserUpdateView, self).get_queryset()
        return qs.filter(id=self.request.user.id)


@method_decorator(login_required(login_url='/login'), name='dispatch')
class ProfileUpdateView(SuccessMessageMixin, UpdateView):
    model = Profile
    form_class = CustomProfileChangeForm
    template_name = "users/update_profile.html"
    success_url = reverse_lazy('users:profile')
    success_message = 'Profile has been updated SuccessFully!'

    def get_queryset(self):
        """ Limit a User to only modifying their own data. """
        qs = super(ProfileUpdateView, self).get_queryset()
        return qs.filter(id=self.request.user.profile.id)
