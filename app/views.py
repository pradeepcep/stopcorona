from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response

from app.models import BedAvailabilityCache
from app.serializers import BedAvailabilitySerializer


class BedAvailabilityViewSet(viewsets.ReadOnlyModelViewSet):
    # Note that we want to query from `BedAvailabilityCache` which is where the current data is.
    # `BedAvailability` is where the historical data lives.
    queryset = BedAvailabilityCache.objects.all().order_by('district', 'institution')
    serializer_class = BedAvailabilitySerializer

    def retrieve(self, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)


def index_page(request):
    return render(request, 'index.html')
