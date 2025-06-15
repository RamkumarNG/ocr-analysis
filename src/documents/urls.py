from django.urls import re_path as url

from rest_framework.routers import SimpleRouter

from .views import DocumentViewSet, JobViewSet

router = SimpleRouter()

router.register(r'documents', DocumentViewSet, basename='documents')
router.register(r'jobs', JobViewSet, basename='job')

urlpatterns = router.urls
