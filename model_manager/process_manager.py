from __future__ import annotations
import shutil
from abc import ABC
from distutils.command.upload import upload
from pathlib import Path
from typing import Any, NamedTuple
from model_manager.process import Process
from werkzeug.wsgi import LimitedStream
import requests

class ProcessManager():

    def __init__(self, file_path):
        self.upload_process_queue = list()
        self.file_path:str = '/temp'
        self.disk_path:str = '/'

    def generate_process_id(self) -> str:
        return "123"

    def create_process(self, process_id: str, file_name: str, description: str) -> :
        if(self.check_file_exist(file_name)):
            pass
        else:
            generate_process_id()

    def check_file_exist(self, file_name: str) -> bool:
        return True

    def load_file_list(self) -> list:
        pass

    
    
    def create(self, process_id: str, file_name: str, description: str, file_path:str) -> process:
        process = Process(process_id, file_name, description, file_path)

    def add_process(self, process: Process):
        if(self.check_process_exist(process.get_process_id())):
            self.upload_process_queue.append(process)

    def set_process_stream(self, process_id: str, file_stream: LimitedStream, file_size: int):
        for process in self.upload_process_queue:
            if(process.get_process_id() == process_id):
                process.set_stream(file_stream)
                break

    def get_process_queue_size(self):
        return len(self.upload_process_queue)

    def check_storage_has_space(self, file_size: float) -> bool:
        total, used, free = shutil.disk_usage(self.disk_path)
        free = free//(2 ** 30)
        return True if (free - file_size) > 5 else False
    
    def check_process_exist(self, process_id: str) -> bool:
        for process in self.upload_process_queue:
            if(process.get_prcess_id() == process_id):
                return True
        return False

    def start_process(self, process_id: int) -> None:
        pass  # TODO: raise process_id not found error

    def is_finish(self, process_id: int) -> bool:
        for process in self.upload_process_queue:
            if(process.get_prcess_id() == process_id):
                return process.is_finish()
        return True

    #notify upload_controller process is finish


class ProcessBase(ABC):

    def __init__(self, process_id: str) -> None:
        self.process_id = process_id


class UploadProcess(ProcessBase):

    def __init__(self, process_id: str, file_name: str, file_path: str,
                 file_stream: Any) -> None:
        super().__init__(process_id)
        self.file_name = file_name
        self.file_path = file_path
        self.file_stream = file_stream  # TODO: type should be updated

        self.progress = 0
