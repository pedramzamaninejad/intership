from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog_list'),
    path('detail/<int:pk>', views.blog_detail_view, name='blog_detail'),
]
