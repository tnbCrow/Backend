from django.db import models


class ChainScanTracker(models.Model):
    total_scans = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.total_scans} at {self.updated_at}'
