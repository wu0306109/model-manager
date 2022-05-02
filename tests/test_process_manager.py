import os
from pathlib import Path

import pytest
from model_manager.process_manager import ProcessManager
from model_manager.process import Process


class TestProcessManager:

    
    def test_create_process(self) -> None:
        manager = ProcessManager()

        file_name = 'name'
        description = 'description'
        process_id = manager.create_process(file_name, description)
        assert type(process_id) == type('')

    def test_check_file_exist(self) -> None:
        manager = ProcessManager()

        file_name = './exist-file.txt'
        assert manager.check_file_exist(file_name)

    def test_load_file_list(self) -> None:
        manager = ProcessManager()

        test_list = manager.load_file_list()
        assert type(test_list) == type([])

    def test_create_process(self) -> None:
        manager = ProcessManager()

        file_name = 'test_file.txt'
        description = 'test'
        process_id = manager.create_process(file_name, description)
        assert type(process_id) == str

        os.remove('./test-file.txt')

    def test_set_stream() -> None:
        pass
        # manager = ProcessManager()
        # file_path = './data/'
        # file_name = 'abc.txt'
        # description = 'test'
        # process = manager.create_process(file_name, description)
        # with open(file_path + file_name, "rb") as file:
        #     process.set_stream(file.stream)
        # assert type(process.get_stream) == type
        

    def test_add_process() -> None:
        manager = ProcessManager()
        
        file_name = 'test_file.txt'
        description = 'test'
        process = manager.create_process(file_name, description)

        origin_size = manager.get_queue_size()
        manager.add_process(process)
        new_size = manager.get_queue_size()
        assert new_size - origin_size == 1
    

