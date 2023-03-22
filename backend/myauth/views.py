from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .models import UserProfile
from .permissions import SignupAccessPolicy
from .serializers import UserSerializer
from .utils import check_recaptcha


class RecaptchaTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        if not check_recaptcha(request.data):
            return Response({"error": "Recaptcha required"})
        else:
            return super(RecaptchaTokenObtainPairView, self).post(request, *args, **kwargs)


class CreateUserView(generics.CreateAPIView):
    model = get_user_model()
    permission_classes = (SignupAccessPolicy,)
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        user = serializer.save()
        try:
            group, _ = Group.objects.get_or_create(name='workers')
            group.user_set.add(user)
        except Exception as e:
            print("Error adding user to group", e)

        # Create profile
        UserProfile.objects.create(user=user)
