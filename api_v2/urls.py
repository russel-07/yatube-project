from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('api/v2/api-token-auth/', obtain_auth_token),
    path('api/v2/posts/', views.APIPost.as_view()),
    path('api/v2/posts/<int:post_id>/', views.APIPostDetail.as_view()),
]