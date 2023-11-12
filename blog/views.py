from django.shortcuts import render
from django.views import generic

from .models import Blog


class BlogListView(generic.ListView):
    queryset = Blog.objects.filter(active=True)
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
