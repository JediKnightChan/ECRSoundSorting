from rest_framework import permissions
from rest_access_policy import AccessPolicy
from common.permissions import ALLOW_OPTIONS_HEAD_TO_AUTH_STATEMENT


class GameFolderAccessPolicy(AccessPolicy):
    statements = [
        ALLOW_OPTIONS_HEAD_TO_AUTH_STATEMENT,
        # Get folders
        {
            "action": ["list", "retrieve"],
            "principal": ["admin", "group:moderators", "group:workers"],
            "effect": "allow"
        }
    ]


class SoundItemAccessPolicy(AccessPolicy):
    statements = [
        ALLOW_OPTIONS_HEAD_TO_AUTH_STATEMENT,
        # Get sounds
        {
            "action": ["list", "retrieve", "get_suggested_categories"],
            "principal": ["admin", "group:moderators", "group:workers"],
            "effect": "allow"
        }
    ]


class SoundCategoryAccessPolicy(AccessPolicy):
    statements = [
        ALLOW_OPTIONS_HEAD_TO_AUTH_STATEMENT,
        # Get sound categories
        {
            "action": ["list", "retrieve"],
            "principal": ["admin", "group:moderators", "group:workers"],
            "effect": "allow"
        }
    ]


class SoundItemReviewAccessPolicy(AccessPolicy):
    statements = [
        ALLOW_OPTIONS_HEAD_TO_AUTH_STATEMENT,
        # Get sound reviews
        {
            "action": ["list", "retrieve"],
            "principal": ["admin", "group:moderators", "group:workers"],
            "effect": "allow"
        },
        # Create, update, destroy sound reviews
        {
            "action": ["create", "update", "partial_update", "destroy"],
            "principal": ["admin", "group:moderators", "group:workers"],
            "effect": "allow"
        },
    ]


class SoundItemReviewModifyPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action in ["update", "partial_update", "destroy"]:
            return request.user.is_authenticated and obj.user_profile.user == request.user
        return True
