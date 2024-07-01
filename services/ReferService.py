from refer_app.models import Refer_Patient
import datetime as dt
from django.db.models import Q
import string
import secrets
from django.conf import settings
from services.EmailService import *

class ReferService():
    ######## User #############

    def generate_referral_code(self):
        alphabet = string.ascii_letters + string.digits
        code = ''.join(secrets.choice(alphabet) for i in range(10))
        return code.upper()

    def sendEmailRefer(self, to, patient_name, referred_by, link, is_existing_user):
        print(to, patient_name, referred_by, link)
        template = settings.REFERRAL_EMAIL_TEMPLATE_SIGNUP
        if is_existing_user:
            template = settings.REFERRAL_EMAIL_TEMPLATE_LOGIN

        message = template\
            .replace("#REFER_LINK#", str(link))\
            .replace("#DR_NAME#", referred_by)\
            .replace("#PATIENT_NAME#",patient_name)
        subject = settings.REFERRAL_SUBJECT_TEMPLATE
        if EmailService.send([to], subject, message):
            return True
        else:
            return False

    def get_all_refers(self, where={}):
        result = Refer_Patient.objects.all().filter(**where)
        print(result.query)
        return result

    def get_refer(self, where={}):
        try:
            result = Refer_Patient.objects.get(**where)

            if result:
                return result

        except Refer_Patient.DoesNotExist:
            return False


    def add_refer(self, data={}):
        Obj = Refer_Patient(**data)
        Obj.save()
        return Refer_Patient.objects.last().refer_patient_id

    def update_refer(self, data, where):
        obj, created = Refer_Patient.objects.update_or_create(
            user_id=where['refer_id'],
            defaults=data,
        )

    def delete_refer(self, where):
        Refer_Patient.objects.filter(**where).update(is_active=0)

    def get_refer_count(self, where={}):
        result = Refer_Patient.objects.filter(**where).count()
        return result


