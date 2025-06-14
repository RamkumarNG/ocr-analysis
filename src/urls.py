from django.urls import path, include

urlpatterns = [
    path('configs/', include('app.configs.urls')),
    path('documents/', include('app.documents.urls')),
]
