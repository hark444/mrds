from django.db import models
from django.utils import timezone

# Create your models here.


class Refer_Patient(models.Model):
    refer_patient_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    mobile_number = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    diagnosis = models.CharField(max_length=50)
    treatment = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    referred_by = models.IntegerField()
    referred_to = models.IntegerField()
    referral_code = models.CharField(max_length=50)
    referred_date = models.DateTimeField(default=timezone.now)
    status = models.IntegerField()

    class Meta:
        db_table = "refer_patient"


