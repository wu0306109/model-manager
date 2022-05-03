from __future__ import annotations
import shutil
from abc import ABC, abstractmethod
from distutils.command.upload import upload
from datetime import datetime
from pathlib import Path
from typing import Any, NamedTuple
from model_manager.process import Process, ProcessResultBase
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

    def __init__(self, file_path):
        self.running_queue = list()
        self.waiting_queue = list()
        self.finish_queue = list()
        self.max_thread_amount = 5
        self.file_path:str = './temp/'
        self.disk_path:str = '/'
        asyncio.run(self.run_running_queue_process())

    # api upload file request
    def upload_file(self, file_name: str, description: str) -> str:
        if self.check_file_exist(file_name):
            return 'file exist'
        if not self.check_storage_has_space():
            return 'space is run out'
        new_process_id = self.generate_process_id()
        new_process = self.create_process(new_process_id, file_name, description, self.file_path)
        self.put_process_into_waiting_queue(new_process)
        return new_process_id

    def check_file_exist(self, file_name: str) -> bool:
        return True # list all file in no sql

    def check_storage_has_space(self, file_size: float) -> bool:
        total, used, free = shutil.disk_usage(self.disk_path)
        free = free//(2 ** 30)
        return True if (free - file_size) > 5 else False

    def generate_process_id(self) -> str:
        return "123"

    def create_process(self, process_id: str, file_name: str, description: str, file_path:str) -> None:
        process = Process(process_id, file_name, description, file_path)
        return process

    def get_process_by_id(self, process_id:str) -> Process:
        for process in self.running_queue:
            if(process.get_prcess_id() == process_id):
                return process
        for process in self.waiting_queue:
            if(process.get_process_id() == process_id):
                return process
        for process in self.finish_queue:
            if(process.get_process_id() == process_id):
                return process
        return None

    def put_process_into_waiting_queue(self, process: Process):
        if(not self.check_process_exist(process.get_process_id())):
            self.waiting_queue.append(process)
    
    #TODO maybe need to throw error
    def check_process_exist(self, process_id: str) -> bool:
        for process in self.running_queue:
            if(process.get_prcess_id() == process_id):
                return True
        for process in self.waiting_queue:
            if(process.get_process_id() == process_id):
                return True
        for process in self.finish_queue:
            if(process.get_process_id() == process_id):
                return True
        return False

    # api set process stream
    def set_process_stream(self, process_id: str, file_stream: LimitedStream) -> str:
        for process in self.waiting_queue:
            if(process.get_process_id() == process_id):
                process.set_stream(file_stream)
                break
          
    def get_running_queue_size(self) -> int:
        return len(self.running_queue)
    
    def get_waiting_queue_size(self) -> int:
        return len(self.waiting_queue)

    #api check progress
    def check_progress(process_id: str) -> float:
        pass

    # run process ascy
    async def run_running_queue_process(self):
        while True:
            asyncio.run(self.move_process_into_running_queue())
            for process in self.running_queue:
                if(not process.get_is_running()):
                    asyncio.run(self.launch_process(process))
            asyncio.run(self.move_process_into_finish_queue())
            # if(len(self.running_queue) == 0 and len(self.waiting_queue) == 0):
            #     break
        return 0
    
    async def move_process_into_running_queue(self):
        while True:
            if(len(self.running_queue) < self.max_thread_amount):
                for i in range(len(self.waiting_queue)):
                    process = self.waiting_queue[i]
                    if(not process.get_is_running() and process.get_stream() != None):
                        self.waiting_queue.remove(i)
                        self.running_queue.append(process)
                        break
            
    async def launch_process(self, process: Process):
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
                    self.move_process_into_finish(process)
                    return 
                file.write(chunk)
    
    async def move_process_into_finish_queue(self):
        while True:
            for i in range(len(self.running_queue)):
                process = self.running_queue[i]
                if(not process.get_is_running() and process.get_id_done()):
                    self.running_queue.remove(i)
                    self.finish_queue.append(process)

    def start_process(self, process_id: int) -> None:
        pass  # TODO: raise process_id not found error

    def is_finish(self, process_id: int) -> bool:
        for process in self.upload_process_queue:
            if(process.get_prcess_id() == process_id):
                return process.is_finish()
        return True

    #notify upload_controller process is finish

