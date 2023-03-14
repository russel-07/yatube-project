from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('api/v3/api-token-auth/', obtain_auth_token),
    path('api/v3/posts/', views.api_posts, name='api_posts'),
    path('api/v3/posts/<int:post_id>/', views.api_posts_detail, name='api_posts_detail'),
]