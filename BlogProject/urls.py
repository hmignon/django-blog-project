from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

urlpatterns = [
    path('', lambda request: redirect('blog/', permanent=False)),
    path('admin/', admin.site.urls),
    path('blog/', include('apps.blog.urls')),
    path('shop/', include('apps.shop.urls')),
]
