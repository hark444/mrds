from django.core.mail import send_mail
from django.conf import settings


class EmailService:

    @staticmethod
    def send(to, subject, message):
        if send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=to,
            html_message=message):
            return True
        else:
            return False
