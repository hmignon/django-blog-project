from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('blog/', views.blog_list, name='list'),
]
