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
        where = ''
        print("user"+str(user_id))
        if user_id:
            where = "AND u.user_id != {0}".format(user_id)
        print("-----"+where)
        query = "select * from ( select u.user_id, u.user_first_name , u.user_last_name, u.profile_image_name,"\
                         " (group_concat(DISTINCT  q.qualification)) as qualification, "\
                         " group_concat(DISTINCT s.specialization) as specialization, "\
                        " up.total_experience, up.about_me, up.consultation_fees,  " \
                        " ua.title, ua.city, ua.state " \
                         " from mrds_v1.user u "\
                         " left join mrds_v1.user_address ua on ua.user_id = u.user_id" \
                        " left join mrds_v1.user_profile up on up.user_id = u.user_id" \
                        " right join user_specialization us on u.user_id = us.user_id"\
                         " left join specialization s on s.specialization_id = us.specialization_id"\
                         " right join user_qualification uq on u.user_id = uq.user_id"\
                         " left join qualification q on q.qualification_id = uq.qualification_id"\
                         " where u.user_type_id in (2, 3) and ua.city LIKE '%%{1}%%' {2}"\
                         " group by u.user_id ) as s1 where specialization  LIKE  '%%{0}%%' or qualification  LIKE  '%%{0}%%' ".format(keyword, city, where)

        print(query)
        result = User.objects.raw(query)
        return result

        ######## Search #############

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



    ######## User clinic availibility ################

    def update_user_clinic_availibiliy(self, data, where):
        obj, created = User_Clinic_Availibility.objects.update_or_create(
            user_id=where['user_id'],day=where['day'],
            defaults=data,
        )


    ######## Search #############
    def get_user_all_info(self, user_id):
        query = "select u.user_id, u.user_first_name , u.user_last_name,  u.profile_image_name," \
                " (group_concat(DISTINCT  q.qualification)) as qualification, " \
                " group_concat(DISTINCT s.specialization) as specialization, " \
                " up.total_experience, up.about_me, up.consultation_fees, " \
                " ua.title,ua.address_1,ua.address_2,ua.pincode, ua.city, ua.state " \
                " from mrds_v1.user u " \
                " left join mrds_v1.user_address ua on ua.user_id = u.user_id" \
                " left join mrds_v1.user_profile up on up.user_id = u.user_id" \
                " left join user_specialization us on u.user_id = us.user_id" \
                " left join specialization s on s.specialization_id = us.specialization_id" \
                " left join user_qualification uq on u.user_id = uq.user_id" \
                " left join qualification q on q.qualification_id = uq.qualification_id" \
                " where  u.user_id = {0} " .format(user_id)

        print(query)
        result = User.objects.raw(query)
        return result[0]

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