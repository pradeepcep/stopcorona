from django.db import models


class BedAvailabilityBase(models.Model):
    '''
    Hospital beds and their availability statuses.
    '''
    # General assumption is for column values: `None` means info wasn't present.
    identifier = models.CharField(max_length=1000, db_index=True)
    district = models.CharField(max_length=500, db_index=True)
    institution = models.CharField(max_length=500, db_index=True)
    covid_beds_total = models.IntegerField(blank=True, null=True)
    covid_beds_occupied = models.IntegerField(blank=True, null=True)
    covid_beds_vacant = models.IntegerField(blank=True, null=True)
    os_beds_total = models.IntegerField('oxygen supported beds total', blank=True, null=True)
    os_beds_occupied = models.IntegerField('oxygen supported beds occupied', blank=True, null=True)
    os_beds_vacant = models.IntegerField('oxygen supported beds vacant', blank=True, null=True)
    nos_beds_total = models.IntegerField('non-oxygen supported beds total', blank=True, null=True)
    nos_beds_occupied = models.IntegerField('non-oxygen supported beds occupied', blank=True, null=True)
    nos_beds_vacant = models.IntegerField('non-oxygen supported beds vacant', blank=True, null=True)
    icu_beds_total = models.IntegerField('ICU beds total', blank=True, null=True)
    icu_beds_occupied = models.IntegerField('ICU beds occupied', blank=True, null=True)
    icu_beds_vacant = models.IntegerField('ICU beds vacant', blank=True, null=True)
    ventilators_total = models.IntegerField(blank=True, null=True)
    ventilators_occupied = models.IntegerField(blank=True, null=True)
    ventilators_vacant = models.IntegerField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True, db_index=True)
    contact_number = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    meta_synced_at = models.DateTimeField(blank=True, null=True, db_index=True)
    meta_last_updated_at = models.DateTimeField(auto_now=True, db_index=True)
    meta_created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.institution} ({self.district}) at {self.meta_synced_at}'


class BedAvailabilityCache(BedAvailabilityBase):
    '''
    Current availability status of hospital beds.
    '''


class BedAvailability(BedAvailabilityBase):
    '''
    Historical availability statuses of hospital beds.
    '''

    class Meta:
        verbose_name_plural = 'bed availabilities'


class SyncPull(models.Model):
    '''
    Script executions to pull beds info.
    '''
    timestamp = models.DateTimeField(auto_now_add=True)
    beds_info = models.JSONField(default=dict)
    meta = models.JSONField(default=dict)  # store success info, error messages etc.

    def __str__(self):
        return f'SyncPull at {self.timestamp}'

    @property
    def created_bed_count(self):
        return self.meta.get('created_bed_count')

    @property
    def created_bed_cache_count(self):
        return self.meta.get('created_bed_cache_count')

    @property
    def sync_start_time(self):
        return self.meta.get('sync_start_time')

    @property
    def sync_end_time(self):
        return self.meta.get('sync_end_time')

    @property
    def sync_time_taken_seconds(self):
        return self.meta.get('sync_time_taken_seconds')
