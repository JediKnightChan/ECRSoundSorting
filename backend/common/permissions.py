# Allow OPTIONS and HEAD requests to authenticated users

ALLOW_OPTIONS_HEAD_TO_AUTH_STATEMENT = {
    "action": ["<method:options>", "<method:head>"],
    "principal": ["authenticated"],
    "effect": "allow",
}
