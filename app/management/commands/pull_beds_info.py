from datetime import datetime

import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse as datetime_parse
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from app.helpers import normalise_institution_name
from app.models import BedAvailability, BedAvailabilityCache, SyncPull


HEADERS = [
    'district', 'institution',
    'covid_beds_total', 'covid_beds_occupied', 'covid_beds_vacant',
    'os_beds_total', 'os_beds_occupied', 'os_beds_vacant',  # Oxygen-supported beds.
    'nos_beds_total', 'nos_beds_occupied', 'nos_beds_vacant',  # Non-oxygen-supported beds.
    'icu_beds_total', 'icu_beds_occupied', 'icu_beds_vacant',
    'ventilators_total', 'ventilators_occupied', 'ventilators_vacant',
    'last_updated', 'contact_number', 'remarks'
]

class Command(BaseCommand):
    help = 'Pull latest beds availability info from various sources'

    @transaction.atomic
    def handle(self, *args, **options):
        start_time = datetime.now()
        self.stdout.write(f'Fetching info page at {settings.BEDS_INFO_URL}...')
        response = requests.get(settings.BEDS_INFO_URL, timeout=settings.REQUEST_TIMEOUT)
        if not response.ok:
            return False, reponse.text

        self.stdout.write(f'Parsing fetched page for beds info...')
        soup = BeautifulSoup(response.text, features='html.parser')
        table = soup.find('table', {'id': 'dtBasicExample'})
        rows = [
            [td.text for td in row.find_all('td')]
            for row in table.select('tr + tr')
        ][1:]  # first row is second line of header, and is empty.

        self.stdout.write(f'Found {len(rows)} beds...')
        result = []
        for row in rows:
            result.append(dict(zip(HEADERS, row)))

        bed_availability_items = []
        bed_availability_cache_items = []
        datetime_now = datetime.now()
        self.stdout.write(f'Syncing timestamp is {datetime_now.isoformat()}...')
        for item in result:
            item['identifier'] = normalise_institution_name(item['institution'])
            item['meta_synced_at'] = datetime_now
            bed_availability_items.append(BedAvailability(**item))
            bed_availability_cache_items.append(BedAvailabilityCache(**item))

        self.stdout.write(f'Writing {len(bed_availability_items)} synced beds to the database table...')
        bed_availability_items = BedAvailability.objects.bulk_create(bed_availability_items)
        created_bed_ids = [item.id for item in bed_availability_items]
        self.stdout.write(f'Done writing beds to the database table...')

        self.stdout.write(f'Emptying the database cache table...')
        BedAvailabilityCache.objects.all().delete()
        self.stdout.write(f'Writing {len(bed_availability_cache_items)} synced beds to the database cache table...')
        bed_availability_cache_items = BedAvailabilityCache.objects.bulk_create(bed_availability_cache_items)
        created_bed_cache_ids = [item.id for item in bed_availability_cache_items]
        self.stdout.write(f'Done writing beds to the database cache table...')

        end_time = datetime.now()
        time_taken_seconds = (end_time - start_time).total_seconds()
        self.stdout.write(f'Writing sync info...')
        SyncPull.objects.create(
            beds_info=rows,
            meta={
                'created_bed_count': len(created_bed_ids),
                'created_bed_ids': created_bed_ids,
                'created_bed_cache_count': len(created_bed_cache_ids),
                'created_bed_cache_ids': created_bed_cache_ids,
                'synced_at': datetime_now.isoformat(),
                'sync_start_time': start_time.isoformat(),
                'sync_end_time': end_time.isoformat(),
                'sync_time_taken_seconds': time_taken_seconds,
            }
        )
        self.stdout.write(f'Done writing sync info. Sync took {time_taken_seconds} seconds...')
        self.stdout.write('All done: beds pulled successfully!')
