from django.urls import path, include
from rest_framework_mongoengine import routers
from .views import BlogPostViewSet

router = routers.DefaultRouter()

router.register(r'news', BlogPostViewSet, basename='news')

urlpatterns = [
    path('', include(router.urls)),
]
