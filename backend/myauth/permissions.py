from rest_access_policy import AccessPolicy


class SignupAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["*"],
            "principal": ["anonymous"],
            "effect": "allow",
        },
    ]
