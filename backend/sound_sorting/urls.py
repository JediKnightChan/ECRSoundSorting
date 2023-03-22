from django.urls import path, include
from rest_framework_mongoengine import routers
from .views import GameFolderViewSet, SoundItemViewSet, SoundCategoryViewSet, SoundItemReviewViewSet

router = routers.DefaultRouter()

router.register(r'folders', GameFolderViewSet, basename='folders')
router.register(r'sounds', SoundItemViewSet, basename='sounds')
router.register(r'categories', SoundCategoryViewSet, basename='categories')
router.register(r'reviews', SoundItemReviewViewSet, basename='reviews')

urlpatterns = [
    path('', include(router.urls)),
]
