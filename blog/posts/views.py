from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# from django.contrib import message


from .models import Post
from .forms import PostForm


class HomeView(TemplateView):
    template_name = "posts/home.html"

@method_decorator(login_required(login_url='/login'), name='dispatch')
class CreatePostView(SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/newpost.html'
    success_url = 'users/profile'
    success_message = 'New post was created SuccessFully!'

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.author = self.request.user
        form.save()
        form.save_m2m()
        return super(CreatePostView, self).form_valid(form)

