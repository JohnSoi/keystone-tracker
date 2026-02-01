import smtplib
from email.message import EmailMessage
from uuid import UUID

from celery import shared_task
from starlette.templating import Jinja2Templates

from app.core.config import AppSettings, get_app_settings

app_settings: AppSettings = get_app_settings()


@shared_task
def send_access_restore_email(user_full_name: str, user_email: str, token: UUID) -> None:
    access_restore_url: str = f"{app_settings.FRONTEND_URL}/restore-access/{token}"

    templates = Jinja2Templates(directory="worker/templates")
    template = templates.get_template("access_restore_email.html")
    html = template.render(
        app_name=app_settings.APP_NAME, access_restore_url=access_restore_url, user_full_name=user_full_name
    )

    message: EmailMessage = EmailMessage()
    message.add_alternative(html, subtype="html")
    message["From"] = app_settings.EMAIL_USERNAME
    message["To"] = user_email
    message["Subject"] = "Восстановление доступа к " + app_settings.APP_NAME

    with smtplib.SMTP_SSL(host=app_settings.EMAIL_HOST, port=app_settings.EMAIL_PORT) as smtp:
        smtp.login(app_settings.EMAIL_USERNAME, app_settings.EMAIL_PASSWORD)
        smtp.send_message(message)
