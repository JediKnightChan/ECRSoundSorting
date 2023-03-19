from .models import BlogPost
from rest_framework.serializers import ModelSerializer


class BlogPostSerializer(ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ["title", "text", "user", "created_timestamp", "last_edited_timestamp", "id"]
