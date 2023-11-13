from django import forms

from .models import Blog, Comment


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'post', 'active')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', 'rate')
