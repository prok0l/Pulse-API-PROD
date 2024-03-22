from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import APIView


class PingView(APIView):
    @staticmethod
    def get(request):
        return HttpResponse("ok", status=status.HTTP_200_OK)


