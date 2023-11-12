from django.shortcuts import render, get_object_or_404
from django.views import generic


from .models import Blog


class BlogListView(generic.ListView):
    queryset = Blog.objects.filter(active=True)
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'


def blog_detail_view(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog/blog_detail.html', {'blog': blog})
