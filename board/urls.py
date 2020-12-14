from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from board.views import PostViewSet, CommentViewSet


router = DefaultRouter()
router.register("post", PostViewSet)
router.register("comment", CommentViewSet)
urlpatterns = router.urls

urlpatterns += [path("api-token-auth/", views.obtain_auth_token)]
