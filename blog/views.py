from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView)
from .models import Post


class PostListView(ListView):
	"""
	This class-based view lists out the posts made by users of the site and paginates them by 5
	"""
	model = Post
	template_name = 'blog/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5


class PostDetailView(DetailView):
	"""
	This class-based view when called, gives an output of a specific post.
	"""
	model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
	"""
	This class-based view is used to create a new post. It takes into consideration the validity of the form.
	"""
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	"""
	This class-based view is used to update a specific post of the website user with an account.
	It has security measures in place to ensure the user is logged in,
	the post is from his own account before an update can be made.
	"""
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
	"""
	This class-based view is used tp delete a specific post of the website user with an account.
	It has security measures in place to ensure the user is logged in,
	the post is from his own account before the post can be deleted.
	
	"""
	model = Post
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


def about(request):
	# This view renders the About page of the website
	return render(request, 'blog/about.html', {'title': 'About'})
