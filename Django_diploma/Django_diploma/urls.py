from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from photo_social_network.views import PostViewSet, CommentViewSet, PostLikeView

r = DefaultRouter()
r.register('posts', PostViewSet)
r.register('comments', CommentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/<int:pk>/like/', PostLikeView.as_view()),
] + r.urls


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)