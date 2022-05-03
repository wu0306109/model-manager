from multiprocessing import Manager
import os
from pathlib import Path
from itsdangerous import NoneAlgorithm
import pytest
from model_manager.process_manager import ProcessManager
from model_manager.process import Process
from werkzeug.wsgi import LimitedStream

class TestProcessManager:
    manager = ProcessManager('./temp/')

    def test_check_file_exist(self) -> None:
        file_name = './exist-file.txt'
        assert self.manager.check_file_exist(file_name)

    def test_check_storage_has_space(self) -> None:
        assert self.manager.check_storage_has_space() > 0

    def test_generate_process_id(self) -> None:
        a = self.manager.generate_process_id()
        b = self.manager.generate_process_id()
        assert a != b

    def test_create_process(self) -> None:
        # manager = ProcessManager()
        file_name = 'name.txt'
        description = 'description'
        file_path = './temp/'
        process = self.manager.create_process(file_name, description)
        assert process.get_file_name() == 'name'
    # def test_load_file_list(self) -> None:
    #     manager = ProcessManager()

    #     test_list = manager.load_file_list()
    #     assert type(test_list) == type([])
    def put_process_into_waiting_queue(self) -> None:
        manager = ProcessManager('./temp/')
        file_name = 'test_file.txt'
        description = 'test'
        process = manager.create_process(file_name, description)

        origin_size = manager.get_waiting_queue_size()
        manager.put_process_into_waiting_queue(process)
        new_size = manager.get_waiting_queue_size()
        assert new_size - origin_size == 1

    def test_set_stream(self) -> None:
        manager = ProcessManager('./temp/')
        file_path = './data/'
        file_name = 'abc.txt'
        description = 'test'
        chunk_size = 3
        file_size = os.stat(file_path + file_name)
        process = manager.create_process(file_name, description)
        with open(file_path + file_name, "rb") as file:
            limited_stream = LimitedStream(file, file_size)
            process.set_stream(limited_stream)
            limited_stream = process.get_stream()
            text = limited_stream.read(chunk_size)
            assert text.decode("utf-8") == "abc"
    
    def test_check_process_exist_false_case(self) -> None:
        manager = ProcessManager('./temp/')
        process_id = '123'
        assert manager.check_process_exist(process_id)

    def test_check_process_exist(self) -> None:
        manager = ProcessManager('./temp/')
        process_id = '123'
        file_name = 'test.txt'
        description = 'content'
        file_path = './temp/'
        process = Process(process_id, file_name, description, file_path)
        manager.put_process_into_waiting_queue(process)
        assert manager.check_process_exist(process_id)

    def test_set_process_stream(self) -> None:
        manager = ProcessManager('./temp/')
        process_id = '123'
        file_path = './data/'
        file_name = 'abc.txt'
        description = 'test'
        chunk_size = 3
        file_size = os.stat(file_path + file_name)
        process = Process(process_id, file_name, description, file_path)
        manager.put_process_into_waiting_queue(process)
        with open(file_path + file_name, "rb") as file:
            limited_stream = LimitedStream(file, file_size)
            manager.set_process_stream(process_id, limited_stream)
            stream = manager.get_process_by_id(process_id)
            assert stream.read(chunk_size) == 'abc'


        
    

