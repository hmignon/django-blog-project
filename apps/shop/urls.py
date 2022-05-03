from django.urls import path

from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.product_list, name='list'),
    path('<int:pk>/<slug:slug>/', views.product_detail, name='detail'),
]
