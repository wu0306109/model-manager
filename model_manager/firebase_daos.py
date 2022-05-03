import firebase_admin
from firebase_admin import credentials

from .process_manager import UploadProcess

cred = credentials.Certificate(
    'secrets/model-manager-349101-firebase-adminsdk-pzrld-ca1a04e3a6.json')
firebase_admin.initialize_app(cred)


class UploadProcessDao:

    def get_process(self, process_id: str) -> UploadProcess:
        pass

    def update_process(self, process: UploadProcess) -> None:
        pass