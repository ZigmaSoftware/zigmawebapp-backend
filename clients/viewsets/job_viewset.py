from rest_framework import viewsets
from clients.models import Job
from clients.serializers.job_serializer import JobSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.filter(is_active=True)
    serializer_class = JobSerializer