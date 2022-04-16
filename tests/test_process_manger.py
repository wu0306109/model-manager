import os
from pathlib import Path

import pytest
from model_manager.process_manager import ProcessManager, UploadProcess


class TestProcessManager:

    def test_create_upload_process(self) -> None:
        manager = ProcessManager()

        with open('./test-file.txt') as stream:
            stream.write('test')

        with open('./test-file.txt') as stream:
            process = manager.create_upload_process('test', Path('./data'),
                                                    stream)

        assert type(process) == type(UploadProcess)

        os.remove('./test-file.txt')

    def test_push_process() -> None:
        manager = ProcessManager()

        with open('./test-file.txt') as stream:
            process = manager.create_upload_process('test', Path('./data'),
                                                    stream)

            manager.push_process(process)

            with pytest.raises(ValueError) as excinfo:
                manager.push_process(process)
