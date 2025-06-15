from django.urls import re_path

from .views import ping
from documents.urls import urlpatterns as document_urlpatterns
from configs.urls import urlpatterns as config_urlpatterns

urlpatterns = [
    re_path(r"^ping$", ping),
]

urlpatterns += document_urlpatterns
urlpatterns += config_urlpatterns
