from django.db import models

# Create your models here.


class BaseStation(models.Model):
    station_identifier = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    recorded_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Common operational status with choices unified to cover both
    OPERATIONAL_STATUSES = [
        ("operational", "Operational"),
        ("maintenance", "Maintenance"),
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]
    operational_status = models.CharField(max_length=20, choices=OPERATIONAL_STATUSES)

    class Meta:
        abstract = True
