import random
from services.EmailService import *
from services.SmsService import *
from django.conf import settings

class OtpService:
    OTP_SUBJECT_TEMPLATE = "OTP to reset your account- MRDS"
    OTP_SMS_TEMPLATE = "Dear user, please use #OTP# to login/signup our application. - MRDS Team"
    OTP_EMAIL_TEMPLATE = "Dear user, please use #OTP# to reset password of your account.\n Thanks,\n MRDS Team"
    REFERRAL_SUBJECT_TEMPLATE = "You have been referred"
    REFERRAL_SMS_TEMPLATE = "Dear user, please use #CODE# to login/signup our application. - MRDS Team"
    REFERRAL_EMAIL_TEMPLATE_SIGNUP = "<html><body>Dear #PATIENT_NAME#,<br>Dr. #DR_NAME# has referred you. please <a href='#REFER_LINK#'>click below link </a> to register yourself in our application " \
                                     "<br><a href='#REFER_LINK#'>#REFER_LINK#<a><br> Thanks,<br> MRDS Team</body></html>"
    REFERRAL_EMAIL_TEMPLATE_LOGIN = "<html><body>Dear #PATIENT_NAME#,<br>Dr. #DR_NAME# has referred you. please <a href='#REFER_LINK#'>click below link </a> to login in our application " \
                                    "<br><a href='#REFER_LINK#'>#REFER_LINK#<a><br> Thanks,<br> MRDS Team</body></html>"
    def __init__(self):
        self.otp = None

    def generate(self):
        self.otp = random.randint(100000, 999999)
        return self.otp

    def sendSmsOtp(self, to):
        message = self.OTP_SMS_TEMPLATE.replace("#OTP#", str(self.otp))
        SmsService.send(to, message)

    def sendEmailOtp(self, to):
        message = self.OTP_EMAIL_TEMPLATE.replace("#OTP#", str(self.otp))
        subject = self.OTP_SUBJECT_TEMPLATE
        if EmailService.send([to], subject, message):
            return True
        else:
            return False



