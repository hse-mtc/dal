from urllib.parse import urlparse

from django.core.mail import send_mail

from conf import settings


def send_regconf_email(
    address: str,
    email: str,
    url: str,
    token: str,
) -> None:
    """Confirm user registration via email.

    Args:
        address: How to address the user receiving this email.
            Example: Ivan Ivanov.

        email: User email.
            Example: ivanov@example.com

        url: URL to the front-end application.
            Example: http://localhost:9999

        token: Valid auth token to embed in the link.
    """

    if "localhost" in url:
        if "http" not in url:
            url = f"http://{url}"
    else:
        if "https" not in url:
            url = f"https://{url}"

    parsed = urlparse(url)
    parsed = parsed._replace(path="change-password")
    parsed = parsed._replace(query=f"token={str(token)}")

    html_message = (f"""
        <p>Здравствуйте, {address}!</p>\n
        
        <p>Ваша регистрация в системе Даль ВУЦ ВШЭ была подтверждена. <br />\n
        Чтобы задать пароль для входа в систему, 
        <a href="{parsed.geturl()}" target="_blank">
            нажмите сюда.
        </a>
        </p>\n
        
        <p>Это письмо было отправлено автоматически; пожалуйста, не отвечайте на него.</p>\n
    """)

    if email.endswith(settings.TEST_CORPORATE_EMAIL_DOMAIN):
        print(html_message)
        return

    send_mail(
        subject="Подтверждение регистрации в системе Даль",
        message=None,  # Send `html_message`.
        from_email=None,  # Django will use `DEFAULT_FROM_EMAIL`.
        recipient_list=[email],
        html_message=html_message,
    )
