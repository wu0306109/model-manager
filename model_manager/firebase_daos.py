from datetime import datetime, timedelta
from typing import List

from firebase_admin import firestore

from model_manager.file_manager import File
from model_manager.process import UploadProcess

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
    
    def get_all_file_name_list(self) -> List[str]:
        docs = self._client.collection('file').stream()
        file_name_list = []
        for doc in docs:
            file_name_list.append(doc.id)
        return file_name_list

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
        ref.set(file_dict)
        ref.set({})
        ref.update(file_dict)

class UploadProcessDao:
    def __init__(self) -> None:
        self.client = firestore.cloent()
    
    def get(self, process_id: str) -> UploadProcess:
        doc = self._client.collection('upload_process').document(process_id).get()

        if not doc.exists:
            raise ValueError(f'Process not exist ({process_id})')
        
        process_dict = doc.to_dict()
        process_id = process_dict['process_id']
        file_path = process_dict['file_path']
        file_name = process_dict['file_name']
        description = process_dict['description']
        process = UploadProcess(process_id, file_path, file_name, description)
        process.set_start_time(process_dict['start_time'])
        process.set_end_time(process_dict['end_time'])
        process.set_is_running(process_dict['is_running'])
        process.set_is_done(process_dict['is_done'])
        process.set_start_time(process_dict['start_time'])
        process.set_file_size(process_dict['file_size'])
        process.set_progress(process_dict['progress'])
        return process

    def get_all_file(self) -> List[str]:
        docs = self._client.collection('upload_process').stream()
        file_name_list = []
        for doc in docs:
            process_dict = doc.to_dict()
            file_name_list.append(process_dict['file_name'])
        return file_name_list

    def get_all_process(self) -> List[str]:
        docs = self._client.collection('upload_process').stream()
        process_id_list = []
        for doc in docs:
            process_id_list.append(doc.id)
        return process_id_list

    def get_all_waiting_process_id(self) -> List[str]:
        docs = self._client.collection('upload_process').stream()
        process_id_list = []
        for doc in docs.list_documents():
            process_dict = doc.to_dict()
            if process_dict.is_running == False and process_dict.is_done == False:
                process_id_list.append(doc.id)
        return process_id_list

    def get_all_running_process_id(self) -> List[str]:
        docs = self._client.collection('upload_process').stream()
        process_id_list = []
        for doc in docs.list_documents():
            process_dict = doc.to_dict()
            if process_dict.is_running == True and process_dict.is_done == False:
                process_id_list.append(doc.id)
        return process_id_list

    def get_all_finish_process_id(self) -> List[str]:
        docs = self._client.collection('upload_process').stream()
        process_id_list = []
        for doc in docs.list_documents():
            process_dict = doc.to_dict()
            if process_dict.is_done == True:
                process_id_list.append(doc.id)
        return process_id_list
    
    def update(self, process: UploadProcess) -> None:
        ref = self._client.collection('upload_process').document(process.get_process_id())
        process_dict = {
            'start_time': process.get_start_time(),
            'end_time' : process.get_end_time(),
            'is_running' : process.get_is_running(),
            'is_done' : process.get_is_done(),
            'file_path' : process.get_file_path(),
            'file_name' : process.get_file_name(),
            'description' : process.get_description(),
            'file_size' : process.get_file_size(),
            'file_progress' : process.get_progress()
        }
        ref.update(process_dict)

    def add(self, process: UploadProcess) -> None:
        ref = self._client.collection('upload_process')
        process_dict = {
            'process_id' : process.get_process_id(),
            'start_time': process.get_start_time(),
            'end_time' : process.get_end_time(),
            'is_running' : process.get_is_running(),
            'is_done' : process.get_is_done(),
            'file_path' : process.get_file_path(),
            'file_name' : process.get_file_name(),
            'description' : process.get_description(),
            'file_size' : process.get_file_size(),
            'file_progress' : process.get_progress()
        }
        ref.document(process.get_process_id()).set(process_dict)
