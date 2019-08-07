from django.contrib import admin
from .models import (Author, Post, Category, Comment, ViewPost)
# Register your models here.
admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(ViewPost)
