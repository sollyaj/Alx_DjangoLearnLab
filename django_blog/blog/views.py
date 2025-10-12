from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Post, Comment, Tag
from django.db.models import Q
from .forms import PostForm, CommentForm


# Home page
def home(request):
    return render(request, 'blog/home.html')

def posts_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    posts = tag.posts.order_by('-published_date').all()
    context = {'tag': tag, 'posts': posts}
    return render(request, 'blog/posts_by_tag.html', context)

# Search view
def search(request):
    q = request.GET.get('q', '').strip()
    posts = Post.objects.none()
    if q:
        posts = Post.objects.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(tags__name__icontains=q)
        ).distinct().order_by('-published_date')
    context = {'query': q, 'posts': posts}
    return render(request, 'blog/search_results.html', context)

# ✅ CRUD VIEWS

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Comments for this post
        context['comments'] = self.object.comments.select_related('author').all()
        # Comment form for authenticated users
        context['comment_form'] = CommentForm()
        return context
    
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    # we don't need a template for create because form is on post_detail page,
    # but Django CreateView expects one if used directly. We'll override post(),
    # so template_name isn't required.

    def post(self, request, *args, **kwargs):
        post_pk = self.kwargs.get('post_pk')
        post = get_object_or_404(Post, pk=post_pk)
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Your comment was added.")
        else:
            messages.error(request, "There was an error with your comment.")
        return redirect('blog:post-detail', pk=post_pk)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        messages.success(self.request, "Comment updated.")
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('blog:post-detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        # ensure author is set and tags saved
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        # if PostForm saved with commit=False earlier, use form.save with commit=True to set tags
        # call form.save(commit=True) to set tags using our overridden save
        form.instance = post
        form.save(commit=True)
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        return form

    def form_valid(self, form):
        # Save post and tags
        post = form.save(commit=False)
        post.save()
        form.instance = post
        form.save(commit=True)
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# ✅ Registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('blog:home')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

# ✅ Profile
@login_required
def profile(request):
    return render(request, 'blog/profile.html')



