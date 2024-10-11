import yadisk


class DiskService:
    """Yandex Disk API wrapper.

    Usage:
        ds = DiskService(token=yadisk_token)
    """

    def __init__(self, token) -> None:
        self._service = yadisk.YaDisk(token=token)

    def obtain_folder(self, path, **kwargs):
        if not self._service.exists(path):
            self._service.mkdir(path, **kwargs)
        return path

    def upload_docx(self, local_path, remote_path, **kwargs):
        with open(local_path, "rb") as f:
            return self._service.upload(f, remote_path, **kwargs)

    def delete_file(self, path, **kwargs):
        self._service.remove(path, **kwargs)

    def read_share_folder_with_anyone(self, remote_path):
        self._service.publish(remote_path)
        public_key = self._service.get_meta(remote_path)["public_key"]
        public_resource = self._service.get_public_meta(public_key)
        return public_resource["public_url"]
