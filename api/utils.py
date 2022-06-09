from django.core.mail import send_mail

from ToolManagmentSystem import settings


def send_email(user, activation_link: str):
    try:
        subject = "welcome!"
        message = f"Hi {user.name}, click here to activate {activation_link}."
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [
            user.email,
        ]
        send_mail(subject, message, email_from, recipient_list)
        return True
    except:
        return False
