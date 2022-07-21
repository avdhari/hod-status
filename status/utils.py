from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, int_to_base36  # noqa
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


def send_password_reset_mail(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    mail_template = 'registration/password_reset.html'
    subject = 'password reset | hod'
    domain = settings.DOMAIN
    password_reset_url = f'{domain}/reset/{uid}/{token}'
    message = "reset password | hod"
    ctx = {
        'password_reset_url': password_reset_url,
        'user': user,
    }
    mail_content = render_to_string(mail_template, ctx)
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email, ], html_message=mail_content)
