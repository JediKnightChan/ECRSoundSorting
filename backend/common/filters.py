import django_filters


class StringInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass
