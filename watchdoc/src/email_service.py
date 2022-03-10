import smtplib
import ssl

from config import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS


class EmailService:
    """Email API wrapper.

    Usage:
        email_service = EmailService()
        email_service.send_message(to, body)
    """

    def __init__(self):
        self.server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        if EMAIL_USE_TLS:
            context = ssl.create_default_context()
            self.server.starttls(context=context)
        self.server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        self.from_user = EMAIL_HOST_USER

    def send_message(self, to, body, **kwargs):
        return self.server.sendmail(self.from_user, [to], body, **kwargs)
