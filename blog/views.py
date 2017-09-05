from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostForm, CommentForm

@login_required
def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
	return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def post_detail(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', post_id=post.pk)
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form, 'mode':'New Post'})

@login_required
def post_edit(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', post_id=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form': form, 'mode':'Edit Post'})

@login_required
def post_delete(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	post.delete()
	return redirect('post_list')

@login_required
def add_comment_to_post(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.save()
			return redirect('post_detail', post_id=post.pk)
	else:
		form = CommentForm()
	return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_delete(request, comment_id):
	comment = get_object_or_404(Comment, pk=comment_id)
	comment.delete()
	return redirect('post_detail', post_id=comment.post.pk)
