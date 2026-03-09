from rest_framework import serializers
from clients.models.job_application import JobApplication
from clients.models import Job
from clients.serializers.job_serializer import JobSerializer


class JobApplicationSerializer(serializers.ModelSerializer):

    job_id = serializers.SlugRelatedField(
        queryset=Job.objects.all(),
        slug_field="unique_id"
    )

    job_details = JobSerializer(source="job_id", read_only=True)

    class Meta:
        model = JobApplication
        fields = [
            "unique_id",
            "job_id",
            "job_details",
            "full_name",
            "phone",
            "email",
            "resume",
            "cover_letter",
            "applied_at"
        ]

        read_only_fields = ["unique_id", "applied_at"]