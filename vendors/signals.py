# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder, Vendor


# @receiver(post_save, sender=PurchaseOrder)
# def calculate_vendor_metrics(sender, instance, created, **kwargs):
#     if instance.status == 'completed':
#         completed_pos = PurchaseOrder.objects.filter(vendor=instance.vendor, status='completed')
#
#         # On-Time Delivery Rate
#         on_time_pos = completed_pos.filter(delivery_date__lte=instance.delivery_date)
#         instance.vendor.on_time_delivery_rate = (on_time_pos.count() / completed_pos.count()) * 100
#
#         # Quality Rating Average
#         completed_pos_with_rating = completed_pos.exclude(quality_rating=None)
#         instance.vendor.quality_rating_avg = completed_pos_with_rating.aggregate(Avg('quality_rating'))[
#             'quality_rating__avg']
#
#         # Average Response Time
#         acknowledged_pos = completed_pos.exclude(acknowledgment_date=None)
#         instance.vendor.average_response_time = acknowledged_pos.aggregate(Avg('acknowledgment_date' - 'issue_date'))[
#             'acknowledgment_date__avg']
#
#         # Fulfilment Rate
#         successful_pos = completed_pos.filter(status='completed', quality_rating__isnull=True)
#         instance.vendor.fulfillment_rate = (successful_pos.count() / completed_pos.count()) * 100
#
#         instance.vendor.save()
