from __future__ import annotations

from abc import ABC
from pathlib import Path
from typing import Any, NamedTuple


class ProcessManager():

    def __init__(self):
        self.upload_process_queue = list()

    def create_upload_process(self, file_name: str, file_path: Path,
                              file_stream: Any) -> ProcessBase:
        pass

    def push_process(self, process: ProcessBase) -> None:  #size
        """Push a process to process manager.

        Args:
            process (ProcessBase): _description_

        Raise:
            ValueError: process exists
        """
        pass

    def start_process(self, process_id: int) -> None:
        pass  # TODO: raise process_id not found error

    def get_queue_size(self) -> int:
        pass

    def is_finish(self, process_id: int) -> bool:
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
