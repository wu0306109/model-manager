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
        self.is_running: bool = False
        self.is_done: bool = False

    def get_process_id(self) -> str:
        return self.process_id
    
    def get_start_time(self) -> float:
        return self.start_time
    
    def set_start_time(self, start_time):
        self.start_time = start_time

    def get_end_time(self) -> float:
        return self.end_time
    
    def set_end_time(self, end_time: float):
        self.end_time = end_time

    def get_is_running(self) -> bool:
        return self.is_running
    
    def set_is_running(self, is_running: bool):
        self.is_running = is_running

    def get_is_done(self) -> bool:
        return self.is_done

    def set_is_done(self, is_done: bool):
        self.is_done = is_done

class UploadProcess(ProcessBase):

    def __init__(self, process_id, file_path, file_name, description):
        ProcessBase.__init__(self, process_id)
        self.file_path: str = file_path
        self.file_name: str = file_name
        self.description: str = description
        self.file_stream: LimitedStream = None
        self.file_size: int = 0
        self.progress: float = 0

    def get_file_path(self) -> str:
        return self.file_path

    def get_file_name(self) -> str:

        return self.file_name

    def get_description(self) -> str:
        return self.description

    def get_stream(self) -> LimitedStream:
        return self.file_stream

    def set_stream(self, file_stream: LimitedStream):
        self.file_stream = file_stream

    def get_file_size(self) -> int:
        return self.file_size
    
    def set_file_size(self, file_size: int):
        self.file_size = file_size

    def get_progress(self) -> float:
        return self.progress

    def set_progress(self, progress: float):
        self.progress = progress
