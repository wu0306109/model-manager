from __future__ import annotations
from operator import truediv
import shutil
from abc import ABC, abstractmethod
from distutils.command.upload import upload
from datetime import datetime
from pathlib import Path
from typing import Any, NamedTuple
from model_manager.process import UploadProcess, ProcessResultBase
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

    def load_waiting_process(self) -> list:
        pass# dao
        
    def load_finish_process(self) -> list:
        pass #dao
    
    def load_running_process(self) -> list:
        pass # dao

    def check_process_in_queue(self, process_id: str, process_queue: list) -> bool:
        for process in process_queue:
            if(process_id == process.get_process_id()):
                return True
        return False

    def get_process_by_id(self, process_id: str) -> UploadProcess:
        pass #DAO
    

    # api upload file request
    def upload_file(self, file_name: str, description: str) -> str:
        if self.check_file_exist(file_name):
            return 'file exist'
        if not self.check_storage_has_space():
            return 'space is run out'
        new_process_id = self.generate_process_id()
        new_process = self.create_process(new_process_id, file_name, description, self.file_path)
        self.save_new_process(new_process)
        return new_process_id

    def save_new_file_process(self, process: UploadProcess):
        pass # dao save file

    def check_file_exist(self, file_name: str) -> bool:
        return True # dao list all file in no sql

    def check_storage_has_space(self, file_size: float) -> bool:
        total, used, free = shutil.disk_usage(self.disk_path)
        free = free//(2 ** 30)
        #dao disk - running process size > 5G
        return True if (free - file_size) > 5 else False

    def generate_process_id(self) -> str:
        return "123"

    def create_process(self, process_id: str, file_name: str, description: str, file_path:str) -> None:
        process = UploadProcess(process_id, file_name, description, file_path)
        return process

    # api set process stream
    def transport_file(self, process_id: str, file_stream: LimitedStream, file_size: int) -> str:
        waiting_process_queue = self.load_waiting_process()
        running_process_queue = self.load_running_process()
        finish_process_queue = self.load_finish_process()
        if(self.check_process_in_queue(process_id, running_process_queue)):
            return 'process is running'
        if(self.check_process_in_queue(process_id, finish_process_queue)):
            return 'process is finish'
        if(not self.check_process_in_queue(process_id, waiting_process_queue)):
            return 'process does not exist'
        if(len(running_process_queue) >= self.max_process_amount):
            return 'wait busy'
        
        process = self.get_process_by_id(self, process_id)
        process.set_stream(file_stream, file_size)
        
        status = self.launch_process(self, process) # TODO status
        if(status):
            return 'upload finish'
        else:
            self.reset_process()
            return 'upload fail'
        


    async def launch_process(self, process: UploadProcess):
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
                    process.set_id_done(True)
                    self.save_process_status(process)
                    break
                self.save_process_status(process)
                file.write(chunk)
            file.close()
    
    def save_process_status(self):
        pass # dao
    
    def reset_process(self):
        pass # reset dao

    #api check progress
    def check_progress(self, process_id) -> str:
        waiting_process_queue = self.load_waiting_process()
        running_process_queue = self.load_running_process()
        finish_process_queue = self.load_finish_process()
        if(self.check_process_in_queue(process_id, running_process_queue)):
            process = self.get_process_by_id(self, process_id)
            return str(process.get_progress())
        if(self.check_process_in_queue(process_id, finish_process_queue)):
            return 'process is finish'
        if(self.check_process_in_queue(process_id, waiting_process_queue)):
            return 'process is waiting'


