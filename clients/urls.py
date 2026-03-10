from django.urls import path
from rest_framework.routers import DefaultRouter
from clients.viewsets.contact_us_viewset import ContactUsViewSet
from clients.viewsets.job_application_viewset import JobApplicationViewSet
from clients.viewsets.job_viewset import JobViewSet
from clients.views import admin_api_login, admin_api_token_login

router = DefaultRouter()
router.register(r'jobs', JobViewSet)
router.register(r'applications', JobApplicationViewSet)
router.register(r'contact-us', ContactUsViewSet)

urlpatterns = [
    path("admin/login/", admin_api_login, name="admin-api-login"),
    path("admin/token-login/", admin_api_token_login, name="admin-api-token-login"),
]
urlpatterns += router.urls
