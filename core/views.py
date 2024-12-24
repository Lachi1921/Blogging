from django.forms import forms
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView, PasswordResetView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import *
from .models import *
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator
from django.contrib.auth import update_session_auth_hash


# Create your views here.


def homepage(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('core:homepage')

    context = {
        'posts': page_obj,
        'form': form
    }

    if page_number:
        return render(request, 'post_list.html', context)
    else:
        return render(request, 'index.html', context)

def register_view(request):
    form = SignUpForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:homepage')
        else:
            print(form.errors)        
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username_or_email = request.POST['username']
            password = request.POST['password']

            users = User.objects.filter(
                Q(username=username_or_email) | Q(email=username_or_email))

            if users.exists():
                user = authenticate(
                    request, username=users[0].username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('core:homepage')

            error_message = 'Invalid username or password.'
            return render(request, 'registration/login.html', {'error_message': error_message})
        else:
            form = LoginForm()
            return render(request, 'registration/login.html', {'form': form})
    else:
        return redirect('core:homepage')

def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')

class CustomPasswordResetView(PasswordResetView):

    def get_success_url(self):
        return reverse_lazy('core:password_reset_done')

    def form_valid(self, form):
        self.request.session['is_initiated'] = True
        return super().form_valid(form)

class CustomPasswordResetDoneView(PasswordResetDoneView):
    def get_success_url(self):
        return reverse_lazy("core:password_reset_complete")

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('is_initiated', False):
            return redirect('core:homepage')
        return super().dispatch(request, *args, **kwargs)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):

    def get_success_url(self):
        return reverse_lazy("core:password_reset_complete")

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('is_initiated', False):
            return redirect('core:homepage')
        return super().dispatch(request, *args, **kwargs)

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('is_initiated', False):
            return redirect('core:homepage')
        return super().dispatch(request, *args, **kwargs)

# posts
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    popular_posts = Post.objects.all().order_by('-created_at')[:3]
    categories = Category.objects.annotate(post_count=Count('post'))
    tags = Tag.objects.all()
    comments = Comment.objects.filter(post=post)
    reply_form = ReplyForm(request.POST or None)
    comment_form = CommentForm(request.POST or None)

    if request.method == 'POST':
        if 'reply' in request.POST and reply_form.is_valid():
            comment = Comment.objects.get(id=request.POST['comment_id'])
            reply = reply_form.save(commit=False)
            reply.post = comment.post
            reply.author = request.user.author
            reply.parent = comment
            reply.save()
            return redirect('core:post_detail', slug=comment.post.slug)
        
        if 'comment' in request.POST and comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user.author
            comment.post = post
            comment.save()
            return redirect('core:post_detail', slug=slug)
    context = {
        'post': post,
        'categories': categories,
        'tags': tags,
        'popular_posts': popular_posts,
        'comments': comments,
        'comment_form': comment_form,
        'reply_form': reply_form,
    }
    return render(request, 'single.html', context)

@login_required(redirect_field_name='next', login_url='/login/')
def post_create_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.author
            post.save()
            form.save_m2m()
            return redirect('core:post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'post_create.html', {'form': form})

@login_required(redirect_field_name='next', login_url='/login/')
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    all_tags = Tag.objects.all()

    if request.user.is_superuser or request.user.author == post.author:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                post = form.save()
                tags = form.cleaned_data['tags']
                post.tags.set(tags)

                messages.success(request, 'Post updated successfully.')
                return redirect('core:post_detail', post.slug)
        else:
            form = PostForm(instance=post)
        return render(request, 'post_edit.html', {'form': form, 'post': post, 'all_tags': all_tags})
    else:
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('core:post_detail', post.slug)


@login_required(redirect_field_name='next', login_url='/login/')
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user.is_superuser or request.user.author == post.author:
        if request.method == 'POST':
            post.delete()
            return redirect('/')
    else:
        messages.error(
            request, 'You do not have permission to edit this post.')
        return redirect('core:post_detail', post.slug)
    return render(request, 'post_delete.html', {'post': post})

def profile_view(request, username):
    user = get_object_or_404(User, username=username)

    author = user.author
    return render(request, 'profile.html', {'author': author})

@login_required(redirect_field_name='next', login_url='/login/')
def settings(request, username):
    if request.user.username == username or request.user.is_superuser:
        author = get_object_or_404(Author, user__username=username)
        user = author.user
        form = ProfileUpdateForm(instance=author)
        password_form = PasswordChangeForm(request.user)
        if request.method == 'POST':
            if request.POST.get('update_profile') is not None:
                form = ProfileUpdateForm(instance=author, data=request.POST, files=request.FILES)
                if form.is_valid():
                    form.save()
                    user.email = form.cleaned_data['email']
                    user.save()
                    messages.success(request, 'Profile updated successfully.')
                    return redirect('core:profile', username=username)
            elif request.POST.get('change_password') is not None:
                password_form = PasswordChangeForm(request.user, request.POST)
                if password_form.is_valid():
                    new_password = password_form.cleaned_data['new_password1']
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Password changed successfully.')
                    return redirect('core:profile', username=username)
                
            elif request.POST.get('delete_account') is not None:
                request.user.delete()
                messages.success(request, 'Ypur account has been deleted.')
                return redirect('core:homepage')
        else:
            return render(request, 'settings.html', {'form': form, 'password_form': password_form})
    else:
        messages.error(request, 'You are not authorized to view this profile.')
        return redirect('core:profile', username=username)

    return render(request, 'settings.html', {'form': form, 'password_form': password_form})

def tag_posts(request, tag_slug):
    posts = Post.objects.filter(tags__name=tag_slug)
    context = {'posts': posts}
    return render(request, 'tag_posts.html', context)

def category_posts(request, category_slug):
    posts = Post.objects.filter(category__name=category_slug)
    category = get_object_or_404(Category, name=category_slug)

    context = {'category': category, 'posts': posts}
    return render(request, 'category_posts.html', context)

def search(request):
    query = request.GET.get('query')
    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query))
    context = {
        'posts': posts,
        'query': query
    }
    return render(request, 'search_results.html', context)
