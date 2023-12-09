from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse_lazy
# from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Blog
from .forms import CommentForm, BlogForm
from .task import send_mail_task


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

    # testing if user is the author of blog
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Blog
    template_name = 'blog/blog_update.html'
    fields = ['title', 'post', 'active']

    # testing if user is the author of blog
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


def blog_create_view(request):
    if request.method == 'POST':
        # blog create form
        blog_form = BlogForm(request.POST)

        if blog_form.is_valid():
            blog = blog_form.save(commit=False)
            blog.author = request.user
            blog.save()

            send_mail_task.delay('Blog Create', f'Your blog was created with the title of {blog.title}',
                      'pzamaninejad.net@gmail.com', [f'{blog.author.email}'])

            return redirect('blog:blog_list')
    else:
        blog_form = BlogForm()

    return render(request, 'blog/blog_create.html', {'form': blog_form})


def user_blogs(request):
    user_blog = Blog.objects.filter(author_id=request.user.id)

    return render(request, 'blog/user_blog.html', {'blogs': user_blog})
