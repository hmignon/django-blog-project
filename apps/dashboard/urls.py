from django.urls import path

from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/new/', views.post_new, name='post_new'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
]
