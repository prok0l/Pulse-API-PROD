from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import APIView

from .models import Countries
from .serializers import CountriesSerializer


class CountriesView(APIView):
    def get(self, request):
        regions = dict(request.GET).get('region', None)
        data = Countries.objects.none()
        if not regions:
            objects = Countries.objects.all()
            data |= objects
        else:
            for region in regions:
                objects = (Countries.objects.filter(region=region)
                           .order_by('alpha2'))
                data |= objects
                if not objects:
                    return JsonResponse({"reason": "Invalid region"},
                                        status=status.HTTP_400_BAD_REQUEST)
        data = data.order_by('alpha2')
        return JsonResponse(CountriesSerializer(data, many=True).data,
                            safe=False, status=status.HTTP_200_OK)


class GetCountryView(APIView):
    def get(self, request, alpha2):
        obj = Countries.objects.filter(alpha2__iexact=alpha2).first()
        if not obj:
            return JsonResponse(
                {"reason": "Страна с указанным кодом не найдена."},
                status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse(CountriesSerializer(obj).data,
                                status=status.HTTP_200_OK)
