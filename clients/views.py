from datetime import timedelta

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def admin_api_login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"detail": "Both username and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(request=request._request, username=username, password=password)
    if user is None:
        return Response(
            {"detail": "Invalid username or password."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if not user.is_staff:
        return Response(
            {"detail": "Only admin/staff users can use this endpoint."},
            status=status.HTTP_403_FORBIDDEN,
        )

    login(request._request, user)
    return Response(
        {"detail": "Login successful.", "username": user.get_username()},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def admin_api_token_login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"detail": "Both username and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(request=request._request, username=username, password=password)
    if user is None:
        return Response(
            {"detail": "Invalid username or password."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if not (user.is_staff or user.is_superuser):
        return Response(
            {"detail": "Only admin/super-admin users can get access tokens."},
            status=status.HTTP_403_FORBIDDEN,
        )

    Token.objects.filter(user=user).delete()
    token = Token.objects.create(user=user)
    now = timezone.now()
    token_ttl_hours = getattr(settings, "TOKEN_TTL_HOURS", 2)
    expires_at = token.created + timedelta(hours=token_ttl_hours)
    return Response(
        {
            "access_token": token.key,
            "token_type": "Token",
            "username": user.get_username(),
            "token_created_at": token.created.isoformat(),
            "token_expires_at": expires_at.isoformat(),
            "server_time": now.isoformat(),
            "token_age_seconds": int((now - token.created).total_seconds()),
            "expires_in_seconds": int((expires_at - now).total_seconds()),
        },
        status=status.HTTP_200_OK,
    )
