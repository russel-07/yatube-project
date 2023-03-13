from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('api/v1/posts', views.APIPostViewSet)


urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_post, name='new_post'),
    path('follow/', views.follow_index, name='follow_index'),
    path('api-token-auth/', obtain_auth_token),
    path('api/v2/posts/', views.api_posts, name='api_posts'),
    path('api/v3/posts/', views.APIPost.as_view()),
    path('api/v2/posts/<int:post_id>/', views.api_posts_detail, name='api_posts_detail'),
    path('api/v3/posts/<int:post_id>/', views.APIPostDetail.as_view()),
    path('<str:username>/', views.profile, name='profile'), # Профайл пользователя
    path('<str:username>/<int:post_id>/', views.post_view, name='post'), # Просмотр записи
    path('<str:username>/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('<str:username>/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('group/<slug:slug>/', views.group_posts, name='group'),
    path('<str:username>/follow/', views.profile_follow, name='profile_follow'), 
    path('<str:username>/unfollow/', views.profile_unfollow, name='profile_unfollow'),
    path('', include(router.urls)),
]