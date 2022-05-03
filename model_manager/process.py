from werkzeug.wsgi import LimitedStream
from abc import ABC, abstractmethod
from datetime import datetime

class ProcessResultBase:

    def __init__(self, initiator: str, start: datetime, end: datetime) -> None:
        self._initiator = initiator  # TODO: to be update for role management
        self._start = start
        self._end = end

    @abstractmethod
    def describe(self) -> str:
        """Describe process result in string for logging."""
        pass

class ProcessBase(ABC):

    def __init__(self, process_id: str) -> None:
        self.process_id = process_id
        self.start_time:float = datetime.now().timestamp()
        self.end_time:float = None

    def set_process_done_time(self):
        self.end_time = datetime.now().timestamp()
    
    def get_start_time(self):
        return self.start_time
    
    def get_start_time(self):
        return self.end_time

class Process(ProcessBase):

    def __init__(self, process_id, file_name, description, file_path):
        self.process_id: str = process_id
        self.file_name: str = file_name
        self.description: str = description
        self.file_path: str = file_path
        self.file_stream: LimitedStream = None
        self.file_size: int = 0
        self.progress: float = 0
        self.is_running: bool = False
        self.is_done: bool = False
    
    def get_process_id(self):
        return self.process_id
    
    def get_file_name(self):
        return self.file_name

    def get_stream(self) -> LimitedStream:
        return self.file_stream

    def set_stream(self, file_stream: LimitedStream, file_size: int):
        self.file_stream = file_stream
        self.file_size = file_size

    def get_file_size(self) -> int:
        return self.file_size

    def set_progress(self, progress: float):
        self.progress = progress

    def get_progress(self) -> float:
        return self.progress
    
    def get_is_running(self) -> bool:
        return self.is_running
    
    def set_is_running(self, is_running: bool) -> bool:
        self.is_running = is_running

    def get_id_done(self) -> bool:
        return self.is_doen

    def set_id_done(self, is_done: bool):
        self.is_doen = is_done
    