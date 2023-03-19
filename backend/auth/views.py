from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response

from .utils import check_recaptcha


class RecaptchaTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        if not check_recaptcha(request.data):
            return Response({"error": "Recaptcha required"})
        else:
            return super(RecaptchaTokenObtainPairView, self).post(request, *args, **kwargs)
