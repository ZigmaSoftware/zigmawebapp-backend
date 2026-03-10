from rest_framework import viewsets
from clients.models import ContactUs
from clients.serializers.contact_us_serializer import ContactUsSerializer


class ContactUsViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.filter(is_active=True)
    serializer_class = ContactUsSerializer
    lookup_field = "unique_id"