from web_app.models import User, User_Type, User_Address, \
    User_Profile, User_Qualification, User_Specialization, \
    Qualification, Specialization, Subscription, User_Subscription,\
    User_Clinic_Availibility, User_Appointment, User_Payment, User_Patient_Refer
import datetime as dt
from django.db.models import Q




class UserService():

    ######## User #############
    def get_all_users(self, where={}):
        result = User.objects.all().filter(**where)
        print(result.query)
        return result

    def get_user(self, where={}):
        try:
            user = User.objects.get(**where)
            if user:
                return user

        except User.DoesNotExist:
            return False

    def add_user(self, data={}):
        Obj = User(**data)
        Obj.save()
        return User.objects.last().user_id

    def update_user(self, data, where):
        obj, created = User.objects.update_or_create(
            user_id=where['user_id'], is_active=1,
            defaults=data,
        )

    def delete_user(self, where):
        User_Address.objects.filter(**where).update(is_active=0)


    ######## Profile ##########

    def get_user_profile(self, where):
        try:
            user = User_Profile.objects.get(**where)

            if user:
                return user
            else:
                return False
        except User_Profile.DoesNotExist:
            return False

    def update_user_profile(self, data, where):
        obj, created = User_Profile.objects.update_or_create(
            user_id=where['user_id'], is_active=1,
            defaults=data,
        )

    def add_user_profile(self, data={}):
        Obj = User_Profile(**data)
        Obj.save()


    ######## Address #############
    def get_user_address(self, where):
        try:
            user = User_Address.objects.get(**where)

            if user:
                return user
            else:
                return False
        except User_Address.DoesNotExist:
            return False


    def update_user_address(self, data, where):
        obj, created = User_Address.objects.update_or_create(
            user_id=where['user_id'], is_active=1,
            defaults=data,
        )

    #### Qualification ########
    def get_qualification(self, where={"is_active": 1}, field=[]):
        result = Qualification.objects.filter(**where)
        if field:
            result.values(*field)

        if result:
            return result
        else:
            return False

    def get_user_qualification(self, where={"is_active": 1}, field=[]):
        result = User_Qualification.objects.filter(**where)
        if field:
            result.values(*field)

        if result:
            return result
        else:
            return False

    def add_user_qualification(self, data):
        Obj = User_Qualification(**data)
        Obj.save()

    def delete_user_qualification(self, where):
        User_Qualification.objects.filter(**where).delete()



    #### Specialization ########
    def get_specialization(self, where={"is_active": 1}, field=[]):
        result = Specialization.objects.filter(**where)
        if field:
            result.values(*field)
        if result:
            return result
        else:
            return False

    def get_user_specialization(self, where={"is_active": 1}, field=[]):
        result = User_Specialization.objects.filter(**where)
        if field:
            result.values(*field)
        if result:
            return result
        else:
            return False

    def get_user_specialization_name(self, where={"is_active": 1}, field=[]):
        result = User_Specialization.objects.filter(**where).select_related('Specialization')
        print(result.query)
        if field:
            result.values(*field)
        if result:
            return result
        else:
            return False


    def add_user_specialization(self, data):
        Obj = User_Specialization(**data)
        Obj.save()

    def delete_user_specialization(self, where):
        User_Specialization.objects.filter(**where).delete()

    ######## Search #############
    def search_user(self, keyword, city, user_id=None):
        if keyword or city or user_id:
            specialization_obj = Specialization.objects.filter(specialization__contains=keyword).values_list(
                'specialization_id', flat=True
            )
            user_specialization_obj = User_Specialization.objects.filter(specialization_id__in=specialization_obj)

            user_obj = User.objects.filter(user_specialization__in=user_specialization_obj)
            if user_id:
                user_obj = user_obj.exclude(user_id=user_id)

            all_user_data = []
            for user in user_obj:
                user_data = dict()
                user_data['user_id'] = user.user_id
                user_data['user_first_name'] = user.user_first_name
                user_data['user_last_name'] = user.user_last_name
                user_data['profile_image_name'] = user.profile_image_name

                # User Qualification Data
                qualification_queryset = user.user_qualification.first()
                if qualification_queryset:
                    user_data['qualification'] = qualification_queryset.qualification

                # User Specialization Data
                specialization_values = Specialization.objects.filter(
                    specialization_id__in=specialization_obj).values_list('specialization', flat=True)
                user_data['specialization'] = ', '.join(specialization_values)

                # User Profile Data
                user_profile_queryset = user.user_profile_set.first()
                if user_profile_queryset:
                    user_data['total_experience'] = user_profile_queryset.total_experience
                    user_data['about_me'] = user_profile_queryset.about_me
                    user_data['consultation_fees'] = user_profile_queryset.consultation_fees

                # User Address Data
                user_address_queryset = user.user_address_set.first()
                if user_address_queryset:
                    user_data['title'] = user_address_queryset.title
                    user_data['address_1'] = user_address_queryset.address_1
                    user_data['address_2'] = user_address_queryset.address_2
                    user_data['pincode'] = user_address_queryset.pincode
                    user_data['city'] = user_address_queryset.city
                    user_data['state'] = user_address_queryset.state

                all_user_data.append(user_data)

            return all_user_data
        else:
            return ""


    def referred_doctor_list(self):
        query = "select * from ( select u.user_id, u.user_first_name , u.user_last_name, u.profile_image_name," \
                " (group_concat(DISTINCT  q.qualification)) as qualification, " \
                " group_concat(DISTINCT s.specialization) as specialization, " \
                " up.total_experience, up.about_me, up.consultation_fees,  " \
                " ua.title, ua.city, ua.state " \
                " from mrds_v1.user u " \
                " left join mrds_v1.user_address ua on ua.user_id = u.user_id" \
                " left join mrds_v1.user_profile up on up.user_id = u.user_id" \
                " right join user_specialization us on u.user_id = us.user_id" \
                " left join specialization s on s.specialization_id = us.specialization_id" \
                " right join user_qualification uq on u.user_id = uq.user_id" \
                " left join qualification q on q.qualification_id = uq.qualification_id" \
                " where  ua.city LIKE '%%{1}%%' {2}" \
                " group by u.user_id ) as s1 where specialization  LIKE  '%%{0}%%' or qualification  LIKE  '%%{0}%%' ".format(
            keyword, city, where)

        print(query)
        result = User.objects.raw(query)
        return result

    ######### Subscription ##########

    def get_subscription(self, where={"is_active": 1}, field=[]):
        result = Subscription.objects.filter(**where)
        if field:
            result.values(*field)
        if result:
            return result
        else:
            return False

    def get_user_subscription(self, where={"is_active": 1}, field=[]):
        result = User_Subscription.objects.filter(**where)
        if field:
            result.values(*field)
        if result:
            return result
        else:
            return False

    def get_user_clinic_availibility(self, where={"is_active": 1}, field=[]):
        result = User_Clinic_Availibility.objects.filter(**where)
        if field:
            result.values(*field)
        if result:
            return result
        else:
            return False

    def update_user_subscription(self, data, where):
        obj, created = User_Subscription.objects.update_or_create(
            user_id=where['user_id'], is_active=1,
            defaults=data,
        )

    def delete_user_subscription(self, where):
        User_Subscription.objects.filter(**where).delete()

    def update_user_clinic_availibiliy(self, data, where):
        obj, created = User_Clinic_Availibility.objects.update_or_create(
            user_id=where['user_id'],day=where['day'],
            defaults=data,
        )

    @staticmethod
    def get_user_all_info(user_id):
        user_obj = User.objects.filter(user_id=user_id).prefetch_related().first()
        user_data = {'user_id': user_id}

        if user_obj:
            # User Data
            user_data['user_first_name'] = user_obj.user_first_name
            user_data['user_last_name'] = user_obj.user_last_name
            user_data['profile_image_name'] = user_obj.profile_image_name

            # User Qualification Data
            qualification_queryset = user_obj.user_qualification.first()
            if qualification_queryset:
                user_data['qualification'] = qualification_queryset.qualification

            # User Specialization Data
            specialization_queryset = user_obj.user_specialization.values_list('specialization_id', flat=True)
            if specialization_queryset:
                specializations = Specialization.objects.filter(specialization_id__in=specialization_queryset).values_list('specialization', flat=True)
                user_data['specialization'] = ', '.join(specializations)

            # User Profile Data
            user_profile_queryset = user_obj.user_profile_set.first()
            if user_profile_queryset:
                user_data['total_experience'] = user_profile_queryset.total_experience
                user_data['about_me'] = user_profile_queryset.about_me
                user_data['consultation_fees'] = user_profile_queryset.consultation_fees

            # User Address Data
            user_address_queryset = user_obj.user_address_set.first()
            if user_address_queryset:
                user_data['title'] = user_address_queryset.title
                user_data['address_1'] = user_address_queryset.address_1
                user_data['address_2'] = user_address_queryset.address_2
                user_data['pincode'] = user_address_queryset.pincode
                user_data['city'] = user_address_queryset.city
                user_data['state'] = user_address_queryset.state

        return user_data

    @staticmethod
    def time_slots(start, end, duration):
        start_time = dt.datetime.strptime(start, '%H:%M')
        end_time = dt.datetime.strptime(end, '%H:%M')
        time_interval = dt.datetime.strptime(duration, '%M')
        time_zero = dt.datetime.strptime('00:00', '%H:%M')
        timeslots = []
        while end_time > start_time:
              end = ((start_time - time_zero + time_interval))
              timeslot = f'{(start_time).time() }'
              h, m, s = timeslot.split(":")
              timeslots.append('{0}:{1}'.format(h, m))
              start_time = end
        return timeslots

    # User appointment
    def set_user_appointment(self, data):
        Obj = User_Appointment(**data)
        Obj.save()
        return Obj.objects.last().user_appointment_id

    def add_or_update_user_appointment(self, data, where):
        user_appointment_id = where['user_appointment_id']
        appointment, created = User_Appointment.objects.update_or_create(
            user_appointment_id=user_appointment_id, is_active=1,
            defaults=data,
        )
        if created:
            return appointment.user_appointment_id
        else:
            return user_appointment_id


    def get_user_appointment(self, where={"is_active": 1}, field=[]):
        result = User_Appointment.objects.filter(**where)
        print(result.query)
        print(result)
        if field:
            result.values(*field)
        if result:
            return result
        else:
            return False

    def get_booked_slot(self, user_id, field=[]):
        result = User_Appointment.objects.filter(Q(is_active = 1),Q(user_id = user_id),
                                                Q(appointment_status=2)
                                              | Q(appointment_status=4)
                                              | Q(appointment_status=5)
                                              | Q(appointment_status=6),)
        print(result.query)
        print(result)
        if field:
            result.values(*field)
        if result:
            return result
        else:
            return False

    def update_user_appointment(self, where, data):
        print(where)
        print(data)
        result = User_Appointment.objects.filter(**where).update(**data)
        print(result.query)

    '''
    1 = USER_PAYMENT_PENDING
    2 = USER_PAYMENT_DONE
    3 = USER_APPT_CANCELLED
    4 = USER_APPT_MODIFIED
    5 = DR_APPT_CONFIRMED
    6 = DR_APPT_MODIFIED
    7 = DR_APPT_CANCELLED
    8 = DR_CONSULT_COMPLETED
    9 = DR_REFERRED
    '''
    def update_user_appointment_status(self, user_appointment_id, status):
        result = User_Appointment.objects.filter(user_appointment_id=user_appointment_id).update(appointment_status=status);

    def update_user_appointment_datetime(self, user_appointment_id, datetime):
        result = User_Appointment.objects.filter(user_appointment_id=user_appointment_id).update(
            appointment_datetime=datetime);

    # User payment
    def set_user_payment(self, data):
        Obj = User_Payment(**data)
        Obj.save()

    def get_user_payment(self, where={"is_active": 1}, field=[]):
        result = User_Payment.objects.filter(**where)
        if field:
            result.values(*field)
        if result:
            return result
        else:
            return False

    def update_user_payment(self, where, data):
        User_Payment.objects.filter(**where).update(**data)

# User payment
    def set_dr_patient_refer(self, data):
        Obj = User_Patient_Refer(**data)
        Obj.save()
        #return Obj.objects.last().user_patient_refer_id

    def get_dr_patient_refer(self, where={"is_active": 1}, field=[]):
        result = User_Patient_Refer.objects.filter(**where)
        if field:
            result.values(*field)
        if result:
            return result
        else:
            return False

    def update__dr_patient_refer(self, where, data):
        User_Patient_Refer.objects.filter(**where).update(**data)


    def is_coupon_applied(self, where={}):
        result = User_Payment.objects.filter(**where).count()
        return result