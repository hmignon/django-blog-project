from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.blog_list, name='list'),
    path('<slug:slug>/', views.blog_by_category, name='category')
]
