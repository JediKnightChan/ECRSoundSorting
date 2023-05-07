from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action

from common.telegram import send_tg_message
from myauth.models import UserProfile

from .filters import GameFolderFilter, SoundItemFilter, SoundItemReviewFilter
from .models import GameFolder, SoundItem, SoundCategory, SoundItemReview
from .serializers import GameFolderSerializer, SoundItemSerializer, SoundCategorySerializer, SoundItemReviewSerializer
from .permissions import GameFolderAccessPolicy, SoundItemAccessPolicy, SoundCategoryAccessPolicy, \
    SoundItemReviewAccessPolicy, SoundItemReviewModifyPermission


class GameFolderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GameFolder.objects.all().order_by('name')
    serializer_class = GameFolderSerializer
    permission_classes = (GameFolderAccessPolicy,)

    filter_backends = [DjangoFilterBackend]
    filterset_class = GameFolderFilter


class SoundItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SoundItem.objects.all().order_by('name')
    serializer_class = SoundItemSerializer
    permission_classes = (SoundItemAccessPolicy,)

    filter_backends = [DjangoFilterBackend]
    filterset_class = SoundItemFilter

    @action(methods=["GET"], detail=True)
    def get_suggested_categories(self, request, *args, **kwargs):
        sound_item = self.get_object()
        q = SoundCategory.objects.filter(sound_reviews__sound=sound_item).annotate(
            nitem=Count('sound_reviews')
        ).order_by('-nitem')[:5]
        catergories = []
        for sc in q:
            catergories.append({ "name": sc.name, "count": sc.nitem })
        return Response({"categories": catergories}, status=status.HTTP_200_OK)


class SoundCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SoundCategory.objects.all().order_by('name')
    serializer_class = SoundCategorySerializer
    permission_classes = (SoundCategoryAccessPolicy,)


class SoundItemReviewViewSet(viewsets.ModelViewSet):
    serializer_class = SoundItemReviewSerializer
    permission_classes = (SoundItemReviewAccessPolicy, SoundItemReviewModifyPermission)

    filter_backends = [DjangoFilterBackend]
    filterset_class = SoundItemReviewFilter

    def perform_create(self, serializer):
        sound_review = serializer.save(user_profile=UserProfile.get_by_user(self.request.user))
        sound_review.sound.update_like_dislike_amount()
        categories = ", ".join([str(c) for c in sound_review.categories.all()])
        send_tg_message(
            f"{self.request.user} reviewed sound {sound_review.sound}: {categories}: https://drive.google.com/uc?id={sound_review.sound.gdrive_id}")

    def perform_update(self, serializer):
        sound_review = serializer.save()
        sound_review.sound.update_like_dislike_amount()
        categories = ", ".join([str(c) for c in sound_review.categories.all()])
        send_tg_message(
            f"{self.request.user} updated sound review {sound_review.sound}: {categories}: https://drive.google.com/uc?id={sound_review.sound.gdrive_id}")

    def get_queryset(self):
        return SoundItemReview.objects.filter(user_profile=UserProfile.get_by_user(self.request.user)).order_by(
            'user_profile')
