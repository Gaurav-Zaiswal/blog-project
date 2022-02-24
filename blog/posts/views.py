import datetime

from django.utils import timezone
from django.utils.timezone import make_aware
from django.views import View
from django.views.generic import ListView, TemplateView, DetailView, DeleteView, UpdateView
from django.views.generic.dates import DateDetailView
from django.views.generic.edit import BaseDeleteView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import HttpResponseRedirect

from .models import Post, Category
from .forms import CategoryForm, PostForm
from users.models import Profile


now_today = datetime.datetime.now()
fifteen_days_back = now_today - timezone.timedelta(days=15)
one_month_back = now_today - timezone.timedelta(days=32)
three_months_back = now_today - timezone.timedelta(days=100)

# setting up local timezone
now_today = make_aware(now_today)
one_month_back = make_aware(one_month_back)
fifteen_days_back = make_aware(fifteen_days_back)
three_months_back = make_aware(three_months_back)


def compute_trend(post_list):
    trending_posts = {}
    for post in post_list:
        trending_posts[post] = post.view_count

    sorted_trending_posts = {k: v for k, v in sorted(trending_posts.items(),
                      key=lambda item: item[1],
                      reverse=True)}

    trending_posts_list = []
    for k in sorted_trending_posts.keys():
        trending_posts_list.append(k)

    return trending_posts_list


class HomeView(ListView):
    model = Post
    template_name = "posts/home.html"
    context_object_name = 'posts_list'

    # def get_queryset(self, *args, **kwargs):
    #     queryset = Post.objects.filter(status=1).order_by('-created_on') # 1: published

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['recent_three'] = Post.objects.filter(status=1).order_by('-created_on')[:3]
        context['popular_this_month'] = Post.objects.filter(
            Q(status=1) & Q(created_on__gte=one_month_back) & Q(created_on__lt=now_today)
        ).order_by('view_count')[:6]
        context['most_popular_posts_list'] = Post.objects.filter(status=1).order_by('view_count')[:6]
        context['recent_except_three'] = Post.objects.filter(status=1).order_by('-created_on')[3:10]
        return context

@method_decorator(login_required(login_url='/login'), name='dispatch')
class CreateCategoryView(SuccessMessageMixin, CreateView):
    model= Category
    form_class = CategoryForm
    template_name = 'posts/add_category.html'
    success_url = reverse_lazy('users:profile')
    success_message = 'Category has been added successfully'

    def form_valid(self, form):
        self.obj = form.save(commit=False)
        self.obj.creator = self.request.user
        form.save()
        return super().form_valid(form)

@method_decorator(login_required(login_url='/login'), name='dispatch')
class CreatePostView(SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/newpost.html'
    success_url = reverse_lazy('users:profile')
    # success_url = '/post / < slug: slug > /'
    success_message = 'New post was created SuccessFully!'

    def form_valid(self, form):
        self.obj = form.save(commit=False)
        # check whether or not user is eligible to work as per laws of his/her country
        self.obj.author = self.request.user  # set author name dynamically
        # if not self.obj.author.Profile.isEligible:
        #     raise AttributeError(
        #         "You are not Eligible to work as per your country's laws."
        #         "If you thinks that's a mistake then you can update it "
        #         "from your profile's settings'" % self.__class__.__name__
        #     )
        form.save()
        # form.save_m2m()
        return super().form_valid(form)


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

    def get_context_data(self, queryset=None, **kwargs):
        """get the posts which are of same category as of the requested detailed post"""

        # get the category of requested detailed post from its slug field(passed through url)
        if queryset is None:
            queryset = self.get_queryset()
        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
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
            # Get the reqested detailed post from filtered queryset
            obj = queryset.get()
            # Now get its category
            post_category = obj.category
            obj.save()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})

        context = {}
        if self.object:
            context['posts_you_may_like'] = Post.objects.filter(
                Q(status=1) & Q(category=post_category) &
                Q(created_on__gte=three_months_back) &
                Q(created_on__lt=now_today)
            ).order_by('view_count')[:6]

            context['popular_posts'] = Post.objects.filter(status=1).order_by('view_count')[:4]
            print(context['popular_posts'])
            context['recent_posts'] = Post.objects.filter(status=1).order_by('-created_on')[:8]
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
        context.update(kwargs)
        return super().get_context_data(**context)

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
    form_class = PostForm
    success_url = reverse_lazy('users:profile')
    template_name = "posts/update_post.html"
    success_message = 'Post has been updated SuccessFully!'
    date_field = "created_on"
    month_format = '%m'

    def get_queryset(self):
        """ Limit a User to only modifying their own data. """
        qs = super(UpdatePostView, self).get_queryset()
        return qs.filter(author=self.request.user)


@method_decorator(login_required(login_url='/login'), name='dispatch')
class DeletePostView(SuccessMessageMixin, BaseDeleteView):
    """
    Deletion using POSTmethod, because get requires confirmation template, and we are using
    bootstrap's modal for this purpose.
    """
    model = Post
    http_method_names = ['post']
    context_object_name = 'remove_post_confirm_object'
    # template_name = "posts/delete_confirm_post.html"
    success_url = reverse_lazy('users:profile')
    success_message = 'Post has been deleted SuccessFully!'


class LatestView(ListView):
    model = Post
    template_name = "posts/latest_post.html"
    context_object_name = 'posts_list'
    paginate_by = 2


class SearchView(ListView):
    model = Post
    template_name = "posts/search_post.html"
    context_object_name = 'posts_list'
    paginate_by = 2

    def get_queryset(self):
        """
        Post needs number as category.So we need to fetch pk from model 'category' using url argument which is a string
        """
        qs = super().get_queryset()
        c = Category.objects.get(name=self.kwargs['category'])
        return qs.filter(Q(category=c.pk) & Q(status=1)).order_by('-created_on')


class TrendingNewsView(ListView):
    model = Post
    template_name = "posts/trending_posts.html"
    context_object_name = 'posts_list'
    paginate_by = 2

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(Q(status=1) & Q(created_on__gte=three_months_back)).order_by('view_count')


class ReviewListView(ListView):
    model = Post
    template_name = "movies/movie_review.html"
    context_object_name = 'posts_list'
    paginate_by = 2
