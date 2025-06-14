from django.urls import re_path as url

from rest_framework.routers import SimpleRouter

from .views import ConfigViewSet

router = SimpleRouter()

router.register(r'configs', ConfigViewSet, basename='configs')

urlpatterns = router.urls
