from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('<int:pk>/<slug:slug>/', views.post_detail, name='detail'),
]
