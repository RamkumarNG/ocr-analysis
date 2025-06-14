from django.http import Http404

from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Document, Job
from .serializers import DocumentSerializer, DocumentUploadSerializer, JobSerializer
from .permissions import CustomPermission

from .tasks import ping_test_task

@api_view(['GET'])
def ping(request):
    ping_test_task.delay()
    return Response({
        "message": "pong",
        "status": status.HTTP_200_OK
    })


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def list(self, request):
        try:
            documents = self.get_queryset()
            serializer = self.get_serializer(documents, many=True)
                    
            return Response({
                "status": "success",
                "data": {
                    "results": serializer.data
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "failure",
                'data': {
                    "message": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def retrieve(self, request, pk, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({
                "status": "success",
                "data": {
                    "results": serializer.data
                }
            }, status=status.HTTP_200_OK)
        except Http404:
            return Response({
                "status": "failure",
                "message": {
                    "data": 'Document not found.'
                }
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "status": "failure",
                "message": {
                    "data": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        try:
            serializer = DocumentUploadSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                document = serializer.save()
                return Response({
                    "status": "success",
                    "data": {
                        "results": DocumentSerializer(document, context={'request': request}).data,
                    }
                }, status=status.HTTP_200_OK)
            
            return Response({
                "status": "failure",
                'data': {
                    "message": serializer.errors
                }
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                "status": "failure",
                'data': {
                    "message": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk):
        try:
            document = self.get_object()
            document.delete()
            return Response({
                "status": "success",
                "data": {
                    "message": "Document Deleted SuccessFully",
                }
            }, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response({
                "status": "failure",
                "message": {
                    "data": 'Document not found.'
                }
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "status": "failure",
                "message": {
                    "data": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk):
        try:
            document = self.get_object()
            name = request.data.get('name')
            if name is not None:
                document.name = name
                document.save()
                return Response({
                    "status": "success",
                    "data": {
                        "results": self.get_serializer(document, context={'request': request}).data
                    }
                }, status=status.HTTP_204_NO_CONTENT)

            return Response({'detail': 'Only "name" field is allowed.'}, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response({
                "status": "failure",
                "message": {
                    "data": 'Document not found.'
                }
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "status": "failure",
                "message": {
                    "data": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = (CustomPermission, )

    def list(self, request, *args, **kwargs):
        jobs = self.get_queryset()
        serializer = self.get_serializer(jobs, many=True)
        return Response({
            "status": "success",
            "data": {
                "results": serializer.data
            }
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, pk, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({
                "status": "success",
                "data": {
                    "results": serializer.data
                }
            }, status=status.HTTP_200_OK)
        except Http404:
            return Response({
                "status": "failure",
                "message": {
                    "data": 'Job not found.'
                }
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "status": "failure",
                "message": {
                    "data": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
