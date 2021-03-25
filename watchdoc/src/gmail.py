from googleapiclient.discovery import build


class GmailService:
    """Gmail API wrapper.

    Usage:
        gs = GmailService()
        gs.send_message(body)
    """

    def __init__(self, credentials):
        self._service = build("gmail", "v1", credentials=credentials)

    def send_message(self, body, **kwargs):
        return self._service.users().messages().send(
            userId="me",
            body=body,
            **kwargs,
        ).execute()
