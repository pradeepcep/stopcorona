from rest_framework import serializers

from app.models import BedAvailabilityCache


class BedAvailabilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = BedAvailabilityCache
        fields = (
            'identifier', 'district', 'institution', 'covid_beds_total', 'covid_beds_occupied', 'covid_beds_vacant',
            'os_beds_total', 'os_beds_occupied', 'os_beds_vacant', 'nos_beds_total', 'nos_beds_occupied',
            'nos_beds_vacant', 'icu_beds_total', 'icu_beds_occupied', 'icu_beds_vacant', 'ventilators_total',
            'ventilators_occupied', 'ventilators_vacant', 'last_updated', 'contact_number', 'remarks',
        )
        read_only_fields = fields
