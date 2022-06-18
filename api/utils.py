from django.core.mail import send_mail

from ToolManagmentSystem import settings


def send_email(user, activation_link: str):
    try:
        subject = "welcome!"
        message = f"Hi {user.name}, click here to activate {activation_link}"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [
            user.email,
        ]
        send_mail(subject, message, email_from, recipient_list)
        return True
    except:
        return False


def send_password_email(data):
    try:
        subject = data['email_subject']
        message = data['email_body']
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [
            data['to_email'],
        ]
        send_mail(subject, message, email_from, recipient_list)
        return True
    except:
        return False