from rest_framework.routers import DefaultRouter
from clients.viewsets.job_application_viewset import JobApplicationViewSet
from clients.viewsets.job_viewset import JobViewSet

router = DefaultRouter()
router.register(r'jobs', JobViewSet)
router.register(r'applications', JobApplicationViewSet)

urlpatterns = router.urls