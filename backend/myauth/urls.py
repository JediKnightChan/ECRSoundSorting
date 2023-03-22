from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView
from django.views.decorators.csrf import csrf_exempt
from .views import RecaptchaTokenObtainPairView, CreateUserView

urlpatterns = [
    path('signup/', csrf_exempt(CreateUserView.as_view()), name='signup'),
    path('token/', RecaptchaTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
]
