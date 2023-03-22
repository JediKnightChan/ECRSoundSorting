import django_filters
from django.db.models import Q

from common.filters import StringInFilter
from myauth.models import UserProfile
from .models import GameFolder, SoundItem, SoundItemReview


class GameFolderFilter(django_filters.FilterSet):
    type__in = StringInFilter(field_name='type', lookup_expr='in')
    is_root_dir = django_filters.BooleanFilter(field_name='parent_folder', lookup_expr='isnull')

    class Meta:
        model = GameFolder
        fields = ['parent_folder']


class SoundItemFilter(django_filters.FilterSet):
    hide_reviewed = django_filters.BooleanFilter(method='hide_reviewed_filter', label='Hide reviewed')

    class Meta:
        model = SoundItem
        fields = ['parent_folder', 'hide_reviewed']

    def hide_reviewed_filter(self, queryset, *args, **kwargs):
        wants_hide_reviews = args[1]
        if not self.request:
            return queryset
        user_profile = UserProfile.get_by_user(self.request.user)
        if wants_hide_reviews:
            queryset = queryset.filter(~Q(sound_reviews__user_profile=user_profile))
        return queryset


class SoundItemReviewFilter(django_filters.FilterSet):
    class Meta:
        model = SoundItemReview
        fields = ['sound', 'user_profile']
