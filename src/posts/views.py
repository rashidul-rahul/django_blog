from django.shortcuts import render
from .models import Post
from marketing.models import Signup

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
    return render(request, 'blog.html')

def post(request):
    return render(request, 'post.html')
