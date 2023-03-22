import django_filters

from .models import BlogPost


class BlogPostFilter(django_filters.FilterSet):
    created_timestamp = django_filters.DateFromToRangeFilter()
    last_edited_timestamp = django_filters.DateFromToRangeFilter()

    class Meta:
        model = BlogPost
        fields = ['created_timestamp', 'last_edited_timestamp', 'user']
