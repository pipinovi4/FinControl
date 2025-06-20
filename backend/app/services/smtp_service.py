# backend/app/services/smtp_service.py

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from jinja2 import Template
from backend.app.core.settings import settings

RESET_PASSWORD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Reset your password</title>
</head>
<body>
    <h2>🔐 Password Reset Request</h2>
    <p>Hello,</p>
    <p>We received a request to reset your password. Click the link below:</p>
    <p><a href="{{ reset_link }}">Reset Password</a></p>
    <p>This link is valid for 30 minutes.</p>
    <p>If you didn’t request this, just ignore this email.</p>
    <br>
    <p>Regards,<br>FinControl Team</p>
</body>
</html>
"""

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True
)


class SMTPService:
    def __init__(self):
        self.fm = FastMail(conf)

    async def send_password_reset_email(self, to_email: EmailStr, reset_token: str) -> None:
        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"

        html = Template(RESET_PASSWORD_TEMPLATE).render(reset_link=reset_link)

        message = MessageSchema(
            subject="🔐 Reset your FinControl password",
            recipients=[to_email],
            body=html,
            subtype=MessageType.html,
        )

        await self.fm.send_message(message)
