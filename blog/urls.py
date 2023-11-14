from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog_list'),
    path('detail/<int:pk>', views.blog_detail_view, name='blog_detail'),
    path('delete/<int:pk>', views.BlogDeleteView.as_view(), name='blog_delete'),
    path('create/', views.BlogCreateView.as_view(), name='blog_create'),
    path('edit/<int:pk>', views.BlogUpdateView.as_view(), name='blog_update')
]
