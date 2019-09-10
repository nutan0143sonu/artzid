from django.conf import settings
from templated_email import send_templated_mail

def sendEmail(instance):
    try:
        send_templated_mail(
            template_name='verify',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.email],
            context={'email': instance.email,'name':instance.name, "message": "Welcome to ArtizID ",'otp':instance.otp}
        )
    except Exception as e:
        print("Exception",e)
        pass
