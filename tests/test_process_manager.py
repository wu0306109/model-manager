from multiprocessing import Manager
import os
from pathlib import Path
from itsdangerous import NoneAlgorithm
import pytest
from model_manager.process_manager import ProcessManager
from model_manager.process import UploadProcess
from werkzeug.wsgi import LimitedStream

class TestProcessManager:

    def test_load_waiting_process(self) -> None:
        assert True #dao
        
    def test_load_finish_process(self) -> None:
        assert True #dao
    
    def test_load_running_process(self) -> None:
        assert True #dao
    
    def test_check_process_in_queue(self) -> None:
        assert True

    def test_get_process_by_id(self) -> None:
        assert True
    
    # upload_file api test
    def test_upload_file(self) -> None:
        assert True

    def test_save_new_file_process(self) -> None:
        assert True

    def test_check_file_exist(self) -> None:
        manager = ProcessManager()
        file_name = './exist-file.txt'
        assert manager.check_file_exist(file_name)

    def test_check_storage_has_space(self) -> None:
        assert self.manager.check_storage_has_space() > 0

    def test_generate_process_id(self) -> None:
        a = self.manager.generate_process_id()
        b = self.manager.generate_process_id()
        assert a != b

    def test_create_process(self) -> None:
        manager = ProcessManager()
        file_name = 'name.txt'
        description = 'description'
        file_path = './temp/'
        process = self.manager.create_process(file_name, description)
        assert process.get_file_name() == 'name'

    #transport file api test 
    def test_transport_file(self) -> None:
        assert True

    def test_launch_process(self) -> None:
        assert True
    
    def test_save_process_status(self) -> None:
        assert True
    
    def test_reset_process(self)->None:
        assert True

    # check progress
    def test_check_progress(self) -> None:
        assert True


    # upload process test
    def test_set_stream(self) -> None:
        manager = ProcessManager()
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


        
    

