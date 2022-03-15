import smtplib


class EmailService:
    """Email API wrapper.

    Usage:
        email_service = EmailService()
        email_service.send_message(to, body)
    """

    def __init__(self, host, port, host_user, host_password, use_tls):
        self.host = host
        self.port = port
        self.host_user = host_user
        self.host_password = host_password
        self.use_tls = use_tls

    def send_message(self, to, body, **kwargs):
        with smtplib.SMTP(self.host, self.port) as server:
            if self.use_tls:
                server.starttls()
            server.login(self.host_user, self.host_password)
            return server.sendmail(self.host_user, [to], body, **kwargs)
