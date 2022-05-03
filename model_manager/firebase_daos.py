from datetime import datetime
from typing import List

from firebase_admin import firestore

from model_manager.file_manager import File


class FileDao:

    def __init__(self) -> None:
        self._client = firestore.client()

    def get(self, filename: str) -> File:
        """Get a file by name, raise ValueError if not exist."""
        doc = self._client.collection('files').document(filename).get()

        if not doc.exists:
            raise ValueError(f'File not exist ({filename=})')

        file_dict = doc.to_dict()
        file_dict['upload_time'] = datetime.fromtimestamp(
            file_dict['upload_time'])
        file_dict['last_used_time'] = datetime.fromtimestamp(
            file_dict['last_used_time'])
        return File(name=filename, **file_dict)

    def get_all(self) -> List[File]:
        """Get all files."""
        docs = self._client.collection('files').stream()

        files = []
        for doc in docs:
            files.append(self.get(doc.id))

        return files

    def update(self, file: File) -> None:
        """Update file, create new if not exist."""
        ref = self._client.collection('files').document(file.name)
        file_dict = {
            'type': file.type,
            'description': file.description,
            'path': file.path,
            'uploader': file.uploader,
            'upload_time': file.upload_time.timestamp(),
            'last_used_time': file.last_used_time.timestamp(),
        }

        ref.set({})
        ref.update(file_dict)
