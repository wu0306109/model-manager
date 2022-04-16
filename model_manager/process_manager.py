from __future__ import annotations
from typing import NamedTuple, Any
from abc import ABC

class ProcessManager():
    
    def __init__(self):
        self.upload_process_queue = list()
    
    def create_process() -> ProcessBase:
        pass

    def push_process(process: ProcessBase) -> bool: #size
        pass
    
    def start_process(process_id: int) -> None:
        pass # TODO: raise process_id not found error 

    def get_queue_size()->int:
        pass

    def is_finish(process_id: int) -> bool:
        pass
    #notify upload_controller process is finish

class ProcessBase(ABC):

    def __init__(self, process_id: str)->None:
        self.process_id = process_id


class UploadProcess(ProcessBase):

    def __init__(self, process_id: str, file_name: str, file_path: str, file_stream: Any) -> None:
        self.process_id = process_id
        self.file_name = file_name
        self.file_path = file_path
        self.file_stream = file_stream # TODO: type should be updated

        self.progress = 0


