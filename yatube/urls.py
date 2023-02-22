"""yatube URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.flatpages import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls), # раздел администратора
    path('about/', include('django.contrib.flatpages.urls')), # flatpages
    path('auth/', include('users.urls')), # регистрация и авторизация
    path('auth/', include('django.contrib.auth.urls')), # регистрация и авторизация
    path('', include('posts.urls')), # импорт из приложения posts
    path('', include('cd.urls')), # импорт из приложения cd
]


urlpatterns += [
        path('about-author/', views.flatpage, {'url': '/author/'}, name='about'),
        path('about-spec/', views.flatpage, {'url': '/spec/'}, name='terms'),
        path('contacts/', views.flatpage, {'url': '/contacts/'}, name='contacts'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
