import os
from pathlib import Path

import pytest
from model_manager.process_manager import ProcessManager, UploadProcess


class TestProcessManager:

    
    def test_upload_file_requeset(self) -> String:
        manager = ProcessManager()

        file_name = 'name'
        description = 'description'
        process_id = manager.create_process(file_name, description)
        assert type(process_id) == type('')

    def test_create(self) -> None:
        manager = ProcessManager()

        with open('./test-file.txt') as stream:
            stream.write('test')

        with open('./test-file.txt') as stream:
            process = manager.create_upload_process('test', Path('./data'),
                                                    stream)

        assert type(process) == type(UploadProcess)

        os.remove('./test-file.txt')

    def test_setProcess_stream() -> None:
        manager = ProcessManager()

        with open('./test-file.txt') as stream:
            process = manager.create_upload_process('test', Path('./data'),
                                                    stream)

            manager.push_process(process)

            with pytest.raises(ValueError) as excinfo:
                manager.push_process(process)
