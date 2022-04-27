from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, NamedTuple

from .file_manager import File


class ProcessResultBase:

    def __init__(self, initiator: str, start: datetime, end: datetime) -> None:
        self._initiator = initiator  # TODO: to be update for role management
        self._start = start
        self._end = end

    @abstractmethod
    def describe(self) -> str:
        """Describe process result in string for logging."""
        pass


class UploadResult(ProcessResultBase):

    def __init__(self, initiator: str, start: datetime, end: datetime,
                 file: File) -> None:
        super().__init__(initiator, start, end)

        self._file = file

    def describe(self) -> str:
        pass


class ProcessManager():

    def __init__(self):
        self.upload_process_queue = list()

    def request_upload(
        self, file_name: str, file_path: Path, file_stream: Any
    ) -> ProcessBase:  # TODO: typing of file stream should be updated
        pass

    def start(self, process_id: str) -> None:
        pass  # TODO: raise process_id not found error

    def check_progress(self, process_id: str) -> float:
        pass

    def get_result(self, process_id: str) -> ProcessBase:
        pass

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
