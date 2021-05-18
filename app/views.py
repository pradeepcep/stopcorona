import functools

from django.db.models import Q
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response

from app.models import BedAvailabilityCache
from app.serializers import BedAvailabilitySerializer


class BedAvailabilityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BedAvailabilityCache.objects.none()
    serializer_class = BedAvailabilitySerializer

    def get_queryset(self):
        def _vacant_filter(comma_separated_list):
            comma_separated_list = comma_separated_list or ''
            vacant_filter = Q()
            value_filters_map = {
                'covid': Q(covid_beds_vacant__gt=0),
                'oxygen': Q(os_beds_vacant__gt=0),
                'nonoxygen': Q(nos_beds_vacant__gt=0),
                'icu': Q(icu_beds_vacant__gt=0),
                'ventilator': Q(ventilators_vacant__gt=0),
            }
            value_filters_map['any'] = functools.reduce(lambda x, y: x | y, value_filters_map.values())
            for value in comma_separated_list.strip().split(','):
                cleaned_value = value.strip().lower()
                if value_filters_map.get(cleaned_value):
                    vacant_filter |= value_filters_map[cleaned_value]
            return vacant_filter

        query_params_filters_map = {
            'district': lambda x: Q(district__icontains=x),
            'search': lambda x: (Q(institution__search=x) | Q(institution__icontains=x)),
            'vacant': _vacant_filter,
        }
        query_params_of_interst = {
            param: value for param, value in self.request.query_params.items()
            if param in query_params_filters_map
        }
        queryset_filters = [
            query_params_filters_map[param](value) for param, value in query_params_of_interst.items()
        ]

        # Note that we want to query from `BedAvailabilityCache` which is where the current data is.
        # `BedAvailability` is where the historical data lives.
        queryset = BedAvailabilityCache.objects.filter(*queryset_filters).all().order_by('district', 'institution')
        return queryset

    def retrieve(self, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)


def index_page(request):
    return render(request, 'index.html')
