from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

DEFAULT_FILE_FIELDS: str = "id, name, webViewLink"

FOLDER_MIME_TYPE: str = "application/vnd.google-apps.folder"
DOCX_MIME_TYPE: str = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


class DriveService:
    """Google Drive API wrapper.

    Usage:
      ds = DriveService()
      files = ds.list_files()
    """
    def __init__(self, credentials) -> None:
        self._service = build("drive", "v3", credentials=credentials)

    # --------------------------------------------------------------------------
    # Files & folders

    def list_files(self, **kwargs):
        return self._service.files().list(**kwargs).execute()

    def list_folders(self, **kwargs):
        response = self.list_files(**kwargs)
        files = response["files"]
        return [f for f in files if f["mimeType"] == FOLDER_MIME_TYPE]

    def obtain_folder(
        self,
        name,
        fields=DEFAULT_FILE_FIELDS,
        parents=None,
        list_kwargs=None,
        create_kwargs=None,
    ):
        parents = parents or []
        list_kwargs = list_kwargs or {}
        create_kwargs = create_kwargs or {}

        q_mime = f"mimeType = '{FOLDER_MIME_TYPE}'"
        q_name = f"name = '{name}'"

        response = self.list_files(
            q=f"{q_mime} and {q_name}",
            spaces="drive",
            fields=f"files({fields})",
            **list_kwargs,
        )

        if response["files"]:
            return response["files"][0]

        body = {
            "mimeType": FOLDER_MIME_TYPE,
            "name": name,
            "parents": parents,
        }
        body.update(create_kwargs.pop("body", {}))

        return self.create_file(
            body=body,
            fields=fields,
            **create_kwargs,
        )

    def create_file(self, **kwargs):
        return self._service.files().create(**kwargs).execute()

    def upload_docx(self, body, path, **kwargs):
        media = MediaFileUpload(path, mimetype=DOCX_MIME_TYPE)
        return self._service.files().create(
            body=body,
            media_body=media,
            fields=DEFAULT_FILE_FIELDS,
            **kwargs,
        ).execute()

    def delete_file(self, file_id):
        return self._service.files().delete(fileId=file_id).execute()

    # --------------------------------------------------------------------------
    # Permissions

    def list_permissions(self, file_id):
        return self._service.permissions().list(fileId=file_id).execute()

    def create_permission(self, file_id, **kwargs):
        return self._service.permissions().create(
            fileId=file_id,
            **kwargs,
        ).execute()

    def delete_permissions(self, file_id, permission_id):
        return self._service.permissions().delete(
            fileId=file_id,
            permissionId=permission_id,
        ).execute()

    # --------------------------------------------------------------------------
    # Sharing

    def read_share_folder_with_anyone(self, folder_id):
        response = self.list_permissions(file_id=folder_id)
        for perm in response["permissions"]:
            if perm["type"] == "anyone":
                break
        else:
            self.create_permission(
                body={
                    "role": "reader",
                    "type": "anyone",
                },
                file_id=folder_id,
            )
