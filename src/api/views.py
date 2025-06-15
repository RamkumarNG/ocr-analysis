from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from .tasks import ping_test_task


@api_view(['GET'])
def ping(request):
    ping_test_task.delay()
    return Response({
        "message": "pong",
        "status": status.HTTP_200_OK
    })

