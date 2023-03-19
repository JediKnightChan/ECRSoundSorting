from rest_access_policy import AccessPolicy
from common.permissions import ALLOW_OPTIONS_HEAD_TO_AUTH_STATEMENT


class BlogPostAccessPolicy(AccessPolicy):
    statements = [
        ALLOW_OPTIONS_HEAD_TO_AUTH_STATEMENT,
        # Get news
        {
            "action": ["list", "retrieve"],
            "principal": ["admin", "group:moderators", "group:workers"],
            "effect": "allow"
        },
        # Create news and delete them
        {
            "action": ["create", "destroy"],
            "principal": ["admin", "group:moderators"],
            "effect": "allow"
        }
    ]
