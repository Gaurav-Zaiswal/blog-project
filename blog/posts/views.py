import datetime
import pytz

from django.utils import timezone
from django.utils.timezone import make_aware
from django.views.generic import ListView, TemplateView, DetailView, UpdateView, DeleteView
from django.views.generic.dates import DateDetailView
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Post
from .forms import PostForm


now_today = datetime.datetime.now()
one_month_back_from_today = now_today - timezone.timedelta(days=32)

# setting up local timezone
now_today = make_aware(now_today)
one_month_back_from_today = make_aware(one_month_back_from_today)
# print("now today with local time : ", now_today)

class HomeView(ListView):
    model = Post
    template_name = "posts/home.html"
    context_object_name = 'posts_list'

    # def get_queryset(self, *args, **kwargs):
    #     queryset = Post.objects.filter(status=1).order_by('-created_on') # 1: published

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['all_posts_list'] = Post.objects.filter(status=1).order_by('-created_on')
        context['popular_this_month'] = Post.objects.filter(
            Q(status=1) & Q(created_on__gte=one_month_back_from_today) & Q(created_on__lt=now_today)
        ).order_by('view_count')[:6]
        context['most_popular_posts_list'] = Post.objects.filter(status=1).order_by('view_count')[:6]
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


# class DetailPostView(DetailView, ):
#     model = Post
#     context_object_name = 'detailed_post'
#     template_name = "posts/detailpost.html"
#
#     def get_object(self):
#         object = super(DetailPostView, self).get_object()
#         object.view_count += 1
#         object.save()
#         return object


class DetailPostView(DateDetailView):
    """
    Detail view of a single object on a single date; this differs from the
    standard DetailView by accepting a year/month/day in the URL.
    """
    model = Post
    date_field = "created_on"
    month_format = '%m'
    template_name = 'posts/detailpost.html'
    context_object_name = "detailed_post"

    def get_object(self, queryset=None):
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()
        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})
        # If none of those are defined, it's an error.
        if pk is None and slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )
        try:
            # Get the single item from the filtered queryset
            # and increase the view count by one
            obj = queryset.get()
            obj.view_count += 1
            obj.save()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


@method_decorator(login_required(login_url='/login'), name='dispatch')
class UpdatePostView(SuccessMessageMixin, UpdateView):
    model = Post
    fields = ('title', 'category', 'thumbnail_img', 'content', 'status')
    template_name = "posts/update_post.html"
    success_message = 'Post has been updated SuccessFully!'

    def get_queryset(self):
        """ Limit a User to only modifying their own data. """
        qs = super(UpdatePostView, self).get_queryset()
        return qs.filter(owner=self.request.user)


@method_decorator(login_required(login_url='/login'), name='dispatch')
class DeletePostView(SuccessMessageMixin, DeleteView):
    model = Post
    context_object_name = 'remove_post_confirm_object'
    template_name = "posts/delete_confirm_post.html"
    success_url = reverse_lazy('users:profile')
    success_message = 'Post has been deleted SuccessFully!'
