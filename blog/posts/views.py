from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# from django.contrib import message


from .models import Post
from .forms import PostForm


class HomeView(ListView):
    model = Post
    template_name = "posts/home.html"
    context_object_name = 'posts_list'

    # def get_queryset(self, *args, **kwargs):
    #     queryset = Post.objects.filter(status=1).order_by('-created_on') # 1: published

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['all_posts_list'] = Post.objects.filter(status=1).order_by('-created_on')
        context['most_popular_posts_list'] = Post.objects.filter(status=1).order_by('view_count')[:5]
        return context


@method_decorator(login_required(login_url='/login'), name='dispatch')
class CreatePostView(SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/newpost.html'
    success_url = '/users/profile'
    # success_url = '/post / < slug: slug > /'
    success_message = 'New post was created SuccessFully!'

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.author = self.request.user # set author name dinamically
        form.save()
        form.save_m2m()
        return super(CreatePostView, self).form_valid(form)


class DetailPostView(DetailView):
    model = Post
    context_object_name = 'detailed_post'
    template_name = "posts/detailpost.html"

    def get_object(self):
        object = super(DetailPostView, self).get_object()
        object.view_count += 1
        object.save()
        return object


class UpdatePostView(UpdateView):
    model = Post
    fields = ('title', 'category', 'thumbnail_img', 'content', 'status')
    template_name = "posts/update_post.html"