from django.shortcuts import render
from .models import Post, Category
from marketing.models import Signup
from django.core.paginator import Paginator
from django.db.models import Count, Q

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
    recent_post = Post.objects.order_by('-timestamp')
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
    return render(request, 'post.html')
