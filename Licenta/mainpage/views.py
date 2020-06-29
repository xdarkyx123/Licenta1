from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Q
from django.http import Http404

from mainpage.templates.recommendation import Myrecommend
from .models import Movie, Myrating
from django.contrib import messages
from django.db.models import Case, When
import numpy as np
import pandas as pd


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
	ListView, 
	DetailView, 
	CreateView,
	UpdateView,
	DeleteView
)
from .models import Post

# for recommendation
def recommend(request):
	if not request.user.is_authenticated:
		return redirect("login")
	if not request.user.is_active:
		raise Http404
	df=pd.DataFrame(list(Myrating.objects.all().values()))
	# nu=df.
	nu=df.user_id.unique().shape[0]
	current_user_id= request.user.id
	# if new user not rated any movie
	if current_user_id>nu:
		movie=Movie.objects.get(id=15)
		q=Myrating(user=request.user,movie=movie,rating=0)
		q.save()

	print("Current user id: ",current_user_id)
	prediction_matrix,Ymean = Myrecommend()
	my_predictions = prediction_matrix[:,current_user_id-1]+Ymean.flatten()
	pred_idxs_sorted = np.argsort(my_predictions)
	pred_idxs_sorted[:] = pred_idxs_sorted[::-1]
	pred_idxs_sorted=pred_idxs_sorted+1
	print(pred_idxs_sorted)
	preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pred_idxs_sorted)])
	movie_list=list(Movie.objects.filter(id__in = pred_idxs_sorted,).order_by(preserved)[:10])
	return render(request,'web/recommend.html',{'movie_list':movie_list})


# List view
def index(request):
	movies = Movie.objects.all()
	query  = request.GET.get('q')
	if query:
		movies = Movie.objects.filter(Q(title__icontains=query)).distinct()
		return render(request,'web/list.html',{'movies':movies})
	return render(request,'web/list.html',{'movies':movies})


# detail view
def detail(request,movie_id):
	if not request.user.is_authenticated:
		return redirect("login")
	if not request.user.is_active:
		raise Http404
	movies = get_object_or_404(Movie,id=movie_id)
	#for rating
	if request.method == "POST":
		rate = request.POST['rating']
		ratingObject = Myrating()
		ratingObject.user   = request.user
		ratingObject.movie  = movies
		ratingObject.rating = rate
		ratingObject.save()
		messages.success(request,"Your Rating is submited ")
		return redirect("index")
	return render(request,'web/detail.html',{'movies':movies})



def home(request):
	context = {
		'posts': Post.objects.all()
	}
	return render(request, 'mainpage/home.html', context)

class PostListView(ListView):
	model = Post
	template_name = 'mainpage/home.html' #<app>/<model>_<viewtype>.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 4

class UserPostListView(ListView):
	model = Post
	template_name = 'mainpage/user_posts.html' #<app>/<model>_<viewtype>.html'
	context_object_name = 'posts'
	paginate_by = 4

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
	model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False
