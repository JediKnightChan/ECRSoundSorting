from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView
from .views import RecaptchaTokenObtainPairView

urlpatterns = [
    path('token/', RecaptchaTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
]
