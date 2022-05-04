from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.post_list, name='list'),
    path('<slug:slug>/', views.posts_by_category, name='category'),
    path('<int:pk>/<slug:slug>/', views.post_detail, name='detail'),
]
