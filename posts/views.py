from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from datetime import date

from .models import Post, Group
from .forms import PostForm

User = get_user_model()


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10) # показывать по 10 записей на странице
    page_number = request.GET.get('page') # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(request, 'index.html', {'page': page, 'paginator': paginator})


def index2(request):
    keyword = "утро"
    author=User.objects.get(username="leo")
    start_date=date(1854, 7, 7)
    end_date=date(1854, 7, 21)
    posts = Post.objects.filter(text__contains=keyword, author=author, pub_date__range=(start_date, end_date))
    return render(request, "index.html", {"posts": posts})


def index3(request):
    keyword = request.GET.get("q", None)

    if keyword:
        posts = Post.objects.select_related("author", "group").filter(text__contains=keyword)
    else:
        posts = None

    return render(request, "index.html", {"posts": posts, "keyword": keyword})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "group.html", {"group": group, 'page': page, 'paginator': paginator})


@login_required
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('/')
    return render(request, 'new_post.html', {'form': form})



def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    post_count = Post.objects.filter(author=user_profile.pk).count()
    post_list = Post.objects.filter(author=user_profile.pk)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {'user_profile': user_profile, 'post_count': post_count, 'page': page, 'paginator': paginator})
 
 
def post_view(request, username, post_id):
    user_profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, id=post_id)
    post_count = Post.objects.filter(author=user_profile.pk).count()
    return render(request, 'post.html', {'user_profile': user_profile, 'post': post, 'post_count': post_count})


@login_required
def post_edit(request, username, post_id):
    user_profile = get_object_or_404(User, username=username)
    if user_profile.username != request.user.username:
        return redirect(f'/{username}/{post_id}/')   
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect(f'/{username}/{post_id}/')
    return render(request, 'new_post.html', {'form': form, 'post': post, 'edit': True})

