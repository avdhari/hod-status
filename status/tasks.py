from .celery import app


@app.task
def send_password_reset_mail(user_id):
    from .models import User
    from .utils import send_password_reset_mail

    user = User.objects.get(id=user_id)
    send_password_reset_mail(user)
