from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path("", views.blog_list, name="list"),
    path("<slug:category_slug>/<slug:sub_slug>/", views.blog_by_category, name="category")
]
