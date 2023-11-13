from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required

from .models import Blog
from .forms import CommentForm, BlogForm


class BlogListView(generic.ListView):
    queryset = Blog.objects.filter(active=True)
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'


@login_required
def blog_detail_view(request, pk):
    # blog object
    blog = get_object_or_404(Blog, pk=pk)
    # blog comments
    blog_comment = blog.comment.filter('rate')

    # post a comment
    if request.method == 'POST':
        # create comment form object
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # comment user and blog
            new_comment = comment_form.save(commit=False)
            new_comment.blog = blog
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    context = {
        'blog': blog,
        'comments': blog_comment,
        'comment_form': comment_form
    }
    return render(request, 'blog/blog_detail.html', context=context)
