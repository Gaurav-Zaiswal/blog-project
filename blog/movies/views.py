import datetime, pytz
import json

from django.utils import timezone
from django.utils.timezone import make_aware
from django.http.response import JsonResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.db.models import Q
# from django.conf import settings

from .models import MovieRating
from .forms import MovieReviewForm
from posts.models import Post
from posts.views import compute_trend
from blog.settings.base import (TIME_ZONE)


now_today = datetime.datetime.now(tz=pytz.timezone(TIME_ZONE))
fifteen_days_back = now_today - timezone.timedelta(days=15)
one_month_back = now_today - timezone.timedelta(days=32)
three_months_back = now_today - timezone.timedelta(days=100)


@method_decorator(login_required(login_url='/login'), name='dispatch')
class CreateMovieReviewView(SuccessMessageMixin, CreateView):
    model = MovieRating
    form_class = MovieReviewForm
    template_name = 'movies/add_movie_review.html'
    success_url = reverse_lazy('users:profile')
    success_message = 'New review has been created!'

    def form_valid(self, form):
        self.obj = form.save(commit=False)
        print('after commit')
        self.obj.author = self.request.user
        form.save()
        return super().form_valid(form)


class GetMovieReviewList(ListView):
    model = MovieRating
    template_name = "movies/movie_review.html"
    context_object_name = 'movies_list'
    paginated_by = 9

    # def get_queryset(self, *args, **kwargs):
    #     queryset = Post.objects.filter(status=1).order_by('-created_on') # 1: published

    def get_context_data(self, **kwargs):
        context = super(GetMovieReviewList, self).get_context_data(**kwargs)
        context['recent_movies'] = MovieRating.objects.filter(status=1).order_by('-created_on')
        # print(context)
        return context


class GetDetailedMovieReview(DetailView):
    model = MovieRating
    pk_url_kwarg = 'id'
    template_name = "movies/movie_review_detail.html"
    context_object_name = 'movie_review_details'
    
    def get_context_data(self, **kwargs):
        """
        return detailed post, recent reviews and, you may like
        """
        context = super().get_context_data(**kwargs) # get context

        #get trending posts lists
        trending_posts = compute_trend(
            Post.objects.filter(
                Q(status=1) & Q(created_on__gte=one_month_back) & Q(created_on__lt=now_today)
            )
        )

        # add contexts
        context['latest_reviews'] = MovieRating.objects.all().order_by('-created_on')[:5]
        context['Trending_posts'] = trending_posts




def search_movie(request):
    movie_name = request.GET.get('movie_name')
    payload=[]
    if movie_name:
        qs = MovieRating.objects.filter(movie_name__icontains=movie_name).values('movie_name', 'release_date', 'slug')
        for query in qs:
            query['release_date'] = query['release_date'].year

            q = json.dumps(query, default=str)
            payload.append(q)
        return JsonResponse({'status': 200, 'data': payload})  
    return JsonResponse({'status': 500})
