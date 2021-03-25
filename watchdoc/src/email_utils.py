import base64

from email.mime.text import MIMEText

from config import SERVICE_EMAIL


def create_message(to, link):
    message = MIMEText(f"Hello there. Here is your link: {link}")

    message["to"] = to
    message["from"] = SERVICE_EMAIL
    message["subject"] = "Поступление в Военный учебный центр"

    encoded_bytes = base64.urlsafe_b64encode(message.as_bytes())
    encoded = encoded_bytes.decode("utf-8")

    return {"raw": encoded}
