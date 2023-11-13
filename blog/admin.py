from django.contrib import admin

from .models import Blog, Comment


class BlogCommentInline(admin.TabularInline):
    model = Comment
    fields = ['author', 'text', 'rate']


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'active']

    inlines = [
        BlogCommentInline,
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'blog']
