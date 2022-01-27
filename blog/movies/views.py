import datetime
import json
from django.core import serializers
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from django.shortcuts import render
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
from django.db.models import Q, fields
from django.http import HttpResponseRedirect

from .models import MovieRating
from .forms import MovieReviewForm


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
    template_name = "movies/movie_review_detail.html"
    context_object_name = 'movie_review_details'


def get_address(request):
    """sample for search_movie function"""
    address = request.GET.get('address')

    payload = []
    if address:
        fake_address_objects = FakeAddresses.objects.filter(address__icontains=address) # normal search
        # fake_address_objects = FakeAddresses.search().query("match", address=address) # elasticsearch

        for object in fake_address_objects:
            payload.append(object.address)
    

        return JsonResponse({'status': 200, 'data': payload}) 
    return JsonResponse({'status': 500})

# serializer_qs =serializers.serialize('json', query, ensure_ascii=False)

def search_movie(request):
    movie_name = request.GET.get('movie_name')
    # print(movie_title)
    payload=[]
    if movie_name:
        qs = MovieRating.objects.filter(movie_name__icontains=movie_name).values('movie_name', 'slug')
        for query in qs:
            q = json.dumps(query)
            payload.append(q)
        # serializer_qs =serializers.serialize('json', qs, ensure_ascii=False)
        
        return JsonResponse({'status': 200, 'data': payload}) # data must contain an arrar, here it is payload
    return JsonResponse({'status': 500})




# qs_json = json.dumps(qs)
        # length_qs = len(qs)
        # for i in range(0, length_qs):
        #     query = qs[i]
        #     print(query['slug'])
            # serializer_qs =serializers.serialize('json', query, ensure_ascii=False) 
            # payload.append(serializer_qs)
        # for query in qs:
            # print(movie)
            # payload.append(movie.movie_name)
            # serializer_qs =serializers.serialize('json', query, ensure_ascii=False)
            # payload.append(serializer_qs)