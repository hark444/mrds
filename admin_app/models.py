from django.db import models
from django.utils import timezone

class Coupons(models.Model):
    coupon_id = models.AutoField(primary_key=True)
    coupon_name = models.CharField(max_length=50)
    coupon_code = models.CharField(max_length=20)
    coupon_description = models.CharField(max_length=200)
    coupon_value = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    coupon_created_date = models.DateTimeField(default=timezone.now)
    coupon_modified_date = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = "coupons"






