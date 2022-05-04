from __future__ import annotations
from operator import truediv
import shutil
from abc import ABC, abstractmethod
from distutils.command.upload import upload
from pathlib import Path
from typing import Any, NamedTuple

from py import process

from model_manager.process import UploadProcess, ProcessResultBase
from model_manager.firebase_daos import UploadProcessDao, FileDao

from datetime import datetime
import uuid
from werkzeug.wsgi import LimitedStream
import asyncio

# class UploadResult(ProcessResultBase):

#     def __init__(self, initiator: str, start: datetime, end: datetime,
#                  file: File) -> None:
#         super().__init__(initiator, start, end)

#         self._file = file

#     def describe(self) -> str:
#         pass

class ProcessManager():

    def __init__(self):
        # self.process_queue = list()
        self.max_process_amount:int = 5
        self.file_path:str = './temp/'
        self.disk_path:str = '/'
        asyncio.run(self.run_running_queue_process())

    def load_waiting_process_id(self) -> list:
        dao = UploadProcessDao()
        return dao.get_all_waiting_process_id()

    def load_running_process_id(self) -> list:
        dao = UploadProcessDao()
        return dao.get_all_running_process_id()

    def load_finish_process_id(self) -> list:
        dao = UploadProcessDao()
        return dao.get_all_finish_process_id()

    def check_process_in_queue(self, process_id: str, process_queue: list) -> bool:
        return process_id in process_queue

    def get_process_by_id(self, process_id: str) -> UploadProcess:
        dao = UploadProcessDao()
        upload_process = dao.get(process_id)
        return upload_process
    
    # api upload file request
    def upload_file_request(self, file_name: str, description: str) -> str:
        if self.check_file_exist(file_name):
            return 'file exist'
        if not self.check_storage_has_space():
            return 'space is run out'
        new_process_id = self.generate_process_id()
        new_process = self.create_process(new_process_id, self.file_path, file_name, description)
        self.save_new_process(new_process)
        return new_process_id

    def save_new_process(self, process: UploadProcess):
        dao = UploadProcessDao()
        dao.add(process)

    def check_file_exist(self, file_name: str) -> bool: #Todo need fix
        process_dao = UploadProcessDao()
        file_dao = FileDao()
        process_file_list = process_dao.get_all_file()
        file_list = file_dao.get_all_file_name_list()
        if(file_name in file_list):
            if(file_name in process_file_list):
                return True
            return True
        return False

    def check_storage_has_space(self, file_size: float) -> bool:
        total, used, free = shutil.disk_usage(self.disk_path)
        free = free//(2 ** 30)
        waiting_process_id_list = self.load_waiting_process_id()
        files_size = 0
        for id in waiting_process_id_list:
            process = self.get_process_by_id(id)
            file_size += process.get_file_size()
        files_size = files_size//(2 ** 30)
        #disk - running processes'size > 5G return True
        return True if (free - file_size) > 5 else False

    def generate_process_id(self) -> str:
        return str(uuid.uuid4())

    def create_process(self, process_id: str, file_path:str, file_name: str, description: str) -> None:
        process = UploadProcess(process_id, file_path, file_name, description)
        return process

    # api set process stream
    def transport_file(self, process_id: str, file_stream: LimitedStream, file_size: int) -> str:
        waiting_process_id_list = self.load_waiting_process_id()
        running_process_id_list = self.load_running_process_id()
        finish_process_id_list = self.load_finish_process_id()
        if(self.check_process_in_queue(process_id, running_process_id_list)):
            return 'process is running'
        if(self.check_process_in_queue(process_id, finish_process_id_list)):
            return 'process is finish'
        if(not self.check_process_in_queue(process_id, waiting_process_id_list)):
            return 'process does not exist'
        if(len(running_process_id_list) >= self.max_process_amount):
            return 'wait busy'
        
        process = self.get_process_by_id(self, process_id)
        process.set_stream(file_stream)
        process.set_file_size(file_size)
        
        status = self.launch_process(self, process) # TODO status
        if(status):
            return 'upload finish'
        else:
            self.reset_process()
            return 'upload fail'
        
    def launch_process(self, process: UploadProcess):
        process.set_is_running(True)
        chunk_size = 1024
        stream = process.get_stream()
        file_size = process.get_file_size()
        file_name = process.get_file_name()
        with open(self.file_path + file_name, 'bw') as file:
            while True:
                chunk = stream.read(chunk_size)
                progress = stream.tell() / file_size
                process.set_progress(progress)
                if len(chunk) == 0:
                    end_time = datetime.now().timestamp()
                    process.set_end_time(end_time)
                    process.set_progress(1)
                    process.set_is_done(True)
                    process.set_is_running(False)
                    self.save_process_status(process)
                    break
                self.save_process_status(process)
                file.write(chunk)
            file.close()
    
    def save_process_status(self, process: UploadProcess):
        dao = UploadProcessDao()
        dao.add(process)
    
    def reset_process(self, process: UploadProcess):
        dao = UploadProcessDao()
        process.set_end_time(0)
        process.set_is_running(False)
        process.set_is_done(False)
        process.set_progress(0)
        process.set_file_size(0)
        dao.update(process)

    #api check progress
    def check_progress(self, process_id) -> str:
        waiting_process_id_list = self.load_waiting_process_id()
        running_process_id_list = self.load_running_process_id()
        finish_process_id_list = self.load_finish_process_id()
        if(self.check_process_in_queue(process_id, running_process_id_list)):
            process = self.get_process_by_id(self, process_id)
            return str(process.get_progress())
        if(self.check_process_in_queue(process_id, finish_process_id_list)):
            return 'process is finish'
        if(self.check_process_in_queue(process_id, waiting_process_id_list)):
            return 'process is waiting'


