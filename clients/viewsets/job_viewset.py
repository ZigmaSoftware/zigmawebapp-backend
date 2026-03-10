from rest_framework import viewsets
from rest_framework.permissions import BasePermission, SAFE_METHODS
from clients.authentication import ExpiringTokenAuthentication
from clients.models import Job
from clients.serializers.job_serializer import JobSerializer


class IsAdminOrSuperAdminForWrite(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (user.is_staff or user.is_superuser)
        )


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.filter(is_active=True)
    serializer_class = JobSerializer
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [IsAdminOrSuperAdminForWrite]
