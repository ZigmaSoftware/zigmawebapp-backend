from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key)
        token_ttl_hours = getattr(settings, "TOKEN_TTL_HOURS", 2)
        expires_at = token.created + timedelta(hours=token_ttl_hours)

        if timezone.now() >= expires_at:
            raise AuthenticationFailed("Token has expired. Please login again.")

        return user, token
