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

from .models import Movie, MovieRating
from .forms import MovieForm, MovieReviewForm


@method_decorator(login_required(login_url='/login'), name='dispatch')
class AddMovieView(SuccessMessageMixin, CreateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movies/add_movie.html'
    success_url = reverse_lazy('users:profile')
    # success_url = '/post / < slug: slug > /'
    success_message = 'New movie is added SuccessFully!'

    def form_valid(self, form):
        self.obj = form.save(commit=False)
        # check whether or not user is eligible to work as per laws of his/her country
        self.obj.author = self.request.user  # set author name dynamically
        form.save()
        # form.save_m2m()
        return super().form_valid(form)


@method_decorator(login_required(login_url='/login'), name='dispatch')
class CreateMovieReviewView(SuccessMessageMixin, CreateView):
    model = MovieRating
    form_class = MovieReviewForm
    template_name = 'movies/add_movie_review.html'
    success_url = reverse_lazy('users:profile')
    success_message = 'New review has been created!'

    def form_valid(self, form):
        self.obj = form.save(commit=False)
        self.obj.author = self.request.user
        form.save()
        return super().form_valid(form)


# @method_decorator(login_required(login_url='/login'), name='dispatch')
class GetMoviesList(ListView):
    model = Movie
    template_name = "movies/movie_review.html"
    context_object_name = 'movies_list'
    paginated_by = 9

    # def get_queryset(self, *args, **kwargs):
    #     queryset = Post.objects.filter(status=1).order_by('-created_on') # 1: published

    def get_context_data(self, **kwargs):
        context = super(GetMoviesList, self).get_context_data(**kwargs)
        context['recent_movies'] = Movie.objects.filter(status=1).order_by('-created_on')
        # print(context)
        return context