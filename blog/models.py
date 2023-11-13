from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


class Blog(models.Model):
    # title - author - post - dc created - dc modified
    title = models.CharField(max_length=255)
    author = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    post = models.TextField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    active = models.BooleanField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:blog_detail', args=[self.id])


class Comment(models.Model):
    STATUS_CHOICE = (
        ('a', 'Approve'),
        ('na', 'Not Approve'),
        ('w', 'Wait'),
    )

    author = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='comment')
    text = models.CharField(max_length=500)
    datetime_created = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=2, choices=STATUS_CHOICE, default=STATUS_CHOICE[2][0])
