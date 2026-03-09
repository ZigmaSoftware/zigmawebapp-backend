from rest_framework import viewsets
from clients.models.job_application import JobApplication
from clients.serializers.job_application_serializer import JobApplicationSerializer


class JobApplicationViewSet(viewsets.ModelViewSet):

    queryset = JobApplication.objects.all().order_by("-applied_at")

    serializer_class = JobApplicationSerializer

    lookup_field = "unique_id"