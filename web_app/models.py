from django.db import models
from django.utils import timezone


class User_Type(models.Model):
    user_type_id = models.IntegerField()
    user_type = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "user_type"

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    user_first_name = models.CharField(max_length=100)
    user_last_name = models.CharField(max_length=100)
    user_email = models.CharField(max_length=100)
    user_mobile = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    dob = models.CharField(max_length=10)
    profile_image_name = models.CharField(max_length=50, null=True)
    user_created_date = models.DateTimeField(default=timezone.now)
    user_modified_date = models.DateTimeField(default=timezone.now)
    last_login_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    user_type_id = models.SmallIntegerField()
    referral_code = models.CharField(max_length=10,null=True, default=None)

    class Meta:
        db_table = "mrds_user"


class User_Address(models.Model):
    user_address_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    dist = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    pincode = models.IntegerField()
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    address_type = models.SmallIntegerField()
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "user_address"

class User_Profile(models.Model):
    user_profile_id = models.AutoField(primary_key=True)
    about_me = models.TextField(blank=True)
    total_experience = models.IntegerField(default=0)
    consultation_fees = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "user_profile"

class Qualification(models.Model):
    qualification_id = models.AutoField(primary_key=True)
    qualification = models.CharField(max_length=100)
    keywords = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    user_type_id = models.SmallIntegerField()

    class Meta:
        db_table = "qualification"

class Specialization(models.Model):
    specialization_id = models.AutoField(primary_key=True)
    specialization = models.CharField(max_length=100)
    keywords = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    user_type_id = models.SmallIntegerField()

    class Meta:
        db_table = "specialization"

class User_Qualification(models.Model):
    user_qualification_id = models.AutoField(primary_key=True)
    qualification_id = models.CharField(max_length=100)
    documents = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "user_qualification"

class User_Specialization(models.Model):
    user_specialization_id = models.AutoField(primary_key=True)
    specialization_id = models.CharField(max_length=100)
    documents = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "user_specialization"

class Package(models.Model):
    package_id = models.AutoField(primary_key=True)
    package_name = models.CharField(max_length=100)
    details = models.CharField(max_length=255)
    cost = models.IntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "package"

class User_Package(models.Model):
    user_package_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    package_id =  models.IntegerField()
    class Meta:
        db_table = "user_package"

class Subscription(models.Model):
    subscription_id = models.AutoField(primary_key=True)
    subscription_name = models.CharField(max_length=100)
    subscription_details = models.CharField(max_length=255)
    subscription_validity = models.CharField(max_length=255)
    cost = models.IntegerField()
    is_active = models.BooleanField(default=True)
    user_type_id = models.SmallIntegerField()

    class Meta:
        db_table = "subscription"

class User_Subscription(models.Model):
    user_subscription_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    subscription_id = models.IntegerField()
    subscription_start = models.DateTimeField(default=timezone.now)
    subscription_end = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "user_subscription"

class User_Consultation(models.Model):
    user_consult_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    user_consult_by = models.IntegerField()
    action_date = models.DateTimeField(default=timezone.now)
    action = models.CharField(max_length=50)
    comments = models.TextField(blank=True)
    user_referred_to = models.IntegerField(null = True)
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = "user_consultation"


class User_Payment(models.Model):
    user_payment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    appointment_id = models.IntegerField()
    payment_date = models.DateTimeField(default=timezone.now)
    payment_mode = models.CharField(max_length=50)
    payment_amount = models.CharField(max_length=101)
    payment_status = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    txn_id=models.CharField(max_length=50)
    coupon_code = models.CharField(max_length=50,null=True)

    class Meta:
        db_table = "user_payment"

class User_Clinic(models.Model):
    user_clinic_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    address_id = models.IntegerField()
    consultation_fees = models.IntegerField(default=0)
    class Meta:
        db_table = "user_clinic"

class User_Clinic_Availibility(models.Model):
    User_Clinic_Availibility = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    day = models.CharField(max_length=50)
    start_time = models.CharField(max_length=50)
    end_time = models.CharField(max_length=50)
    duration = models.IntegerField()
    is_available = models.BooleanField(default=True)
    class Meta:
        db_table = "user_clinic_availibility"

class User_Appointment(models.Model):
    user_appointment_id = models.AutoField(primary_key=True)
    patient_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    user_clinic_id = models.CharField(max_length=50)
    appointment_datetime = models.DateTimeField(default=timezone.now)
    appointment_type = models.CharField(max_length=50)
    appointment_status = models.IntegerField(default=1)
    payment_type = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = "user_appointment"


class ProfilePic(models.Model):
    profileName = models.CharField(max_length=50)
    profile_Main_Img = models.ImageField(upload_to='images/')

class User_Patient_Refer(models.Model):
    user_patient_refer_id = models.AutoField(primary_key=True)
    user_appointment_id = models.IntegerField()
    patient_id = models.IntegerField()
    user_from =  models.IntegerField()
    user_to =  models.IntegerField()
    refer_notes = models.CharField(max_length=200)
    refer_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = "user_patient_refer"

