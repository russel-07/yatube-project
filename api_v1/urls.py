from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import PostViewSet, CommentViewSet


router = DefaultRouter()
router.register(r'api/v1/posts', PostViewSet)
router.register(r'api/v1/posts/(?P<id>[0-9]+)/comments', CommentViewSet)


urlpatterns = [
    path('api/v1/api-token-auth/', obtain_auth_token),
    path('', include(router.urls)),
]
