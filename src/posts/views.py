from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Author, ViewPost
from .forms import CommentForm, PostForm
from marketing.models import Signup
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.urls import reverse


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def search(request):
    post_list = Post.objects.order_by('-id')
    query = request.GET.get('q')
    if query:
        queryset = post_list.filter(
            Q(title__icontains=query)|
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'queryset':queryset,
    }
    return render(request, 'search.html', context)

def get_count_category():
    categories = Category.objects.all()
    data = []
    for category in categories:
        data.append({'title':category.title, 'count':Post.objects.filter(categories__title=category.title).count()})
    return data

def index(request):
    fetured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[:3]
    if request.method=='POST':
        email = request.POST['email']
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()
    context ={
        'post_data': fetured,
        'latest_post': latest,
    }
    return render(request, 'index.html', context)

def blog(request):
    category_num = get_count_category()
    print(category_num)
    recent_post = Post.objects.order_by('-timestamp')[:3]
    post_list = Post.objects.order_by('-id')
    paginator = Paginator(post_list, 4)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context ={
        'posts': posts,
        'recent_post': recent_post,
        'category_num': category_num,
    }
    return render(request, 'blog.html', context)

def post(request, id):
    post = get_object_or_404(Post, id=id)
    recent_post = Post.objects.order_by('-timestamp')[:3]
    ViewPost.objects.get_or_create(user=request.user, post=post)
    category_num = get_count_category()
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid:
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(post.get_absolute_url())
    context = {
        'form':form,
        'post':post,
        'recent_post':recent_post,
        'category_num':category_num,
    }
    return render(request, 'post.html', context)

def create_post(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid:
            form.instance.author = author
            form.save()
            return redirect(reverse('post', kwargs={
            'id':form.instance.id
            }))
    context = {
        'title':title,
        'form':form,
    }
    return render(request, 'create_post.html', context)


def update_post(request, id):
    title = 'Update'
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid:
            form.instance.author = author
            form.save()
            return redirect(reverse('post', kwargs={
            'id':form.instance.id
            }))
    context = {
        'form':form,
        'title':title
    }
    return render(request, 'create_post.html', context)

def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse('blog'))
