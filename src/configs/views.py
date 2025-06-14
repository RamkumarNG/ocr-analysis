from rest_framework import viewsets

from .models import FormBaseline
from .serializers import FormBaseLineSerializer

class ConfigViewSet(viewsets.ModelViewSet):
    queryset = FormBaseline.objects.all()
    serializer_class = FormBaseLineSerializer
