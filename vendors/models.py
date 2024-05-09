from datetime import timezone

from django.db import models
from django.db.models import Avg
from django.db.models.functions import Coalesce


STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('canceled', 'Canceled'),
)
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    po_number = models.CharField(max_length=50, unique=True)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField(default=1)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number

    def save(self, *args, **kwargs):
        if self.status == 'completed' and not self.acknowledgment_date:
            self.acknowledgment_date = timezone.now()
        super().save(*args, **kwargs)

    def calculate_performance_metrics(self):
        vendor = self.vendor

        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        completed_pos_count = completed_pos.count()
        fulfilled_pos = completed_pos.filter(issue_date__lte=self.delivery_date)
        fulfilled_pos_count = fulfilled_pos.count()

        vendor.on_time_delivery_rate = fulfilled_pos_count / completed_pos_count if completed_pos_count else 0

        quality_ratings = completed_pos.exclude(quality_rating__isnull=True).values_list('quality_rating', flat=True)
        vendor.quality_rating_avg = quality_ratings.aggregate(avg_quality_rating=
                                                              Avg('quality_rating'))['avg_quality_rating'] or 0

        response_times = completed_pos.exclude(acknowledgment_date__isnull=True).annotate(
            response_time=Coalesce(models.F('acknowledgment_date') - models.F('issue_date'), 0)
        ).values_list('response_time', flat=True)
        vendor.average_response_time = sum(response_times) / len(response_times) if response_times else 0

        vendor.fulfillment_rate = fulfilled_pos_count / completed_pos_count if completed_pos_count else 0

        vendor.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.calculate_performance_metrics()


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor} - {self.date}"
