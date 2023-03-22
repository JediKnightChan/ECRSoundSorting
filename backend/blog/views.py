from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets

from .filters import BlogPostFilter
from .models import BlogPost
from .serializers import BlogPostSerializer
from .permissions import BlogPostAccessPolicy


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all().order_by('last_edited_timestamp')
    serializer_class = BlogPostSerializer
    permission_classes = (BlogPostAccessPolicy,)

    filter_backends = [DjangoFilterBackend]
    filterset_class = BlogPostFilter
