from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Blog
from .forms import CommentForm, BlogForm


class BlogListView(generic.ListView):
    queryset = Blog.objects.filter(active=True)
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'


def blog_detail_view(request, pk):
    # blog object
    blog = get_object_or_404(Blog, pk=pk)
    # blog comments
    blog_comment = blog.comment.order_by('-rate', '-datetime_created')
    # post a comment
    if request.method == 'POST':
        # create comment form object
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # comment user and blog
            new_comment = comment_form.save(commit=False)
            new_comment.blog = blog
            new_comment.author = request.user
            new_comment.save()
            return redirect('blog:blog_detail', pk=pk)
    else:
        comment_form = CommentForm()

    context = {
        'blog': blog,
        'comments': blog_comment,
        'comment_form': comment_form
    }
    return render(request, 'blog/blog_detail.html', context=context)


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Blog
    template_name = 'blog/blog_delete.html'
    success_url = reverse_lazy('blog:blog_list')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class BlogCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = BlogForm
    template_name = 'blog/blog_create.html'
    success_url = reverse_lazy('blog:blog_list')
