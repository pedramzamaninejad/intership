from django.test import TestCase, Client
from django.shortcuts import reverse
from django.contrib.auth.models import User

from .models import Blog


class BlogTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='username',
            email='username@example.com',
            password='Usern@me123'
        )
        self.blog1 = Blog.objects.create(
            title='blog1 Test',
            post='This is a active blog',
            active=True,
            author=self.user,
        )
        self.blog2 = Blog.objects.create(
            title='blog2 test',
            post='This is a inactive blog',
            active=False,
            author=self.user
        )

    def test_blog_list(self):
        response1 = self.client.get('')
        response2 = self.client.get(reverse('blog:blog_list'))
        self.assertEquals(response2.status_code, 200)
        self.assertEquals(response1.status_code, 200)
        self.assertContains(response1, self.blog1.title)
        self.assertContains(response2, self.blog1.id)

    def test_blog_detail(self):
        response = self.client.get(reverse('blog:blog_detail', args=[self.blog1.id]))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, self.blog1.title)

    def test_blog_create(self):
        self.client.login(username='username', password='Usern@me123')
        response = self.client.post(reverse("blog:blog_create"), {
            'title': 'new blog',
            'post': 'new test for blog',
            'active': True,
            'author': self.user.id,
        })
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Blog.objects.last().title, "new blog")

    def test_blog_active_system(self):
        response = self.client.get(reverse('blog:blog_list'))
        self.assertContains(response, self.blog1.title)
        self.assertNotContains(response, self.blog2.title)

    def test_blog_update(self):
        self.client.login(username='username', password='Usern@me123')
        response = self.client.post(reverse('blog:blog_update', args=[self.blog1.id]), {
            'title': 'blog1 update',
            'post': 'blog1 update post',
            'active': True,
            'author': self.blog1.author_id,
        })
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Blog.objects.first().title, 'blog1 update')

    def test_blog_list_template(self):
        response = self.client.get(reverse('blog:blog_list'))
        for template in ('blog/blog_list.html', '_base.html'):
            self.assertTemplateUsed(response, template)

    def test_blog_detail_template(self):
        response = self.client.get(reverse('blog:blog_detail', args=[self.blog1.id]))
        for template in ('blog/blog_detail.html', '_base.html'):
            self.assertTemplateUsed(response, template)

    def test_user_blogs_url(self):
        response = self.client.get(reverse('blog:user_blog'))
        self.assertEquals(response.status_code, 200)

    def test_user_blogs_content(self):
        self.client.login(username='username', password='Usern@m123')
        response = self.client.get(reverse('blog:user_blog'))
        self.assertContains(response, 'blog1')
        self.assertContains(response, 'blog2')
