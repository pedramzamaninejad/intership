from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


class Blog(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='blogs')
    post = models.TextField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    active = models.BooleanField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:blog_detail', args=[self.id])


class Comment(models.Model):
    RATE_CHOICE = (
        ('1', 'Very Bad'),
        ('2', 'Bad'),
        ('3', 'Normal'),
        ('4', 'Good'),
        ('5', 'Very Good')
    )

    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comment')
    blog = models.ForeignKey(Blog, on_delete=models.PROTECT, related_name='comment')

    text = models.CharField(max_length=500)
    datetime_created = models.DateTimeField(auto_now_add=True)

    rate = models.CharField(max_length=1, choices=RATE_CHOICE)
