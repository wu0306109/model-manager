from multiprocessing import Manager
from pathlib import Path
from pydoc import describe
from itsdangerous import NoneAlgorithm
import pytest
from model_manager.process_manager import ProcessManager
from model_manager.process import UploadProcess
from werkzeug.wsgi import LimitedStream

import os
from datetime import datetime

class TestProcessManager:

    def test_load_waiting_process(self) -> None:
        manager = ProcessManager()
        processs_id_list = manager.load_waiting_process_id()
        if(processs_id_list != None and len(processs_id_list) > 0):
            process = manager.get_process_by_id()
            assert process.get_is_running() == False and process.get_is_done == False
        assert True
        
    def test_load_finish_process(self) -> None:
        manager = ProcessManager()
        processs_id_list = manager.load_waiting_process_id()
        if(processs_id_list != None and len(processs_id_list) > 0):
            process = manager.get_process_by_id()
            assert process.get_is_done == True
        assert True
    
    def test_load_running_process(self) -> None:
        manager = ProcessManager()
        processs_id_list = manager.load_waiting_process_id()
        if(processs_id_list != None and len(processs_id_list) > 0):
            process = manager.get_process_by_id()
            assert process.get_is_running() == True and process.get_is_done == False
        assert True
    
    def test_check_process_in_queue_not_exist_case(self) -> None:
        manager = ProcessManager()
        process_id = 'not exist'
        assert not manager.check_process_in_queue(process_id, [])

    def test_check_process_in_queue_exist_case(self) -> None:
        manager = ProcessManager()
        process_id = 'exist'
        assert manager.check_process_in_queue(process_id, ['exist'])

    def test_get_process_by_id(self) -> None:
        manager = ProcessManager()
        process_id = 'exist'
        process = manager.get_process_by_id(process_id)
        assert process.get_process_id() == process_id
    
    # upload_file api test
    def test_upload_file_request(self) -> None:
        manager = ProcessManager()
        old_list = manager.load_waiting_process_id()
        file_name = 'test_upload_file'
        description = "description"
        process_id =  manager.upload_file_request(file_name, description)
        process = manager.get_process_by_id(process_id)
        new_list = manager.load_waiting_process_id()
        assert len(new_list) - len(old_list) == 1 and process.get_process_id == process_id

    def test_save_new_file_process(self) -> None:
        manager = ProcessManager()
        process = UploadProcess('test_new', '/temp/', 'test_upload_file', 'description')
        process.end_time(datetime.now.timestamp())
        assert True

    def test_check_file_exist(self) -> None:
        manager = ProcessManager()
        file_name = './exist-file.txt'
        assert manager.check_file_exist(file_name)

    def test_check_storage_has_space(self) -> None:
        manager = ProcessManager()
        assert manager.check_storage_has_space() > 0

    def test_generate_process_id(self) -> None:
        manager = ProcessManager()
        id = manager.generate_process_id()
        id_list = []
        for i in range(100):
            id_list.append(manager.generate_process_id())
        assert id not in id_list

    def test_create_process(self) -> None:
        manager = ProcessManager()
        file_name = 'name.txt'
        description = 'description'
        file_path = './temp/'
        process = manager.create_process(file_name, description)
        assert process.get_file_name() == 'name'

    #transport file api test 
    def test_transport_file(self) -> None:
        manager = ProcessManager()
        process_id = 'abc'
        file_path = './temp/'
        file_name = 'abc.txt'
        description = 'test'
        chunk_size = 3
        file_size = os.stat(file_path + file_name)
        process = manager.create_process(process_id, file_name, description)
        with open(file_path + file_name, "rb") as file:
            limited_stream = LimitedStream(file, file_size)
            process.set_stream(limited_stream)
            limited_stream = process.get_stream()
            text = limited_stream.read(chunk_size)
            assert text.decode("utf-8") == "abc"
        assert True

    def test_launch_process(self) -> None:
        manager = ProcessManager()
        process_id = 'abc'
        file_path = '/temp/'
        file_name = 'abc.txt'
        description = 'test'
        process = manager.create_process(process_id, file_path, file_name, description)
        with open('./data/abc.text', 'rb') as file:
            process.set_stream(LimitedStream(file), os.stat('./data/abc.text'))
        manager.launch_process(process)
        process = manager.get_process_by_id(process_id)
        assert process.get_is_done() and process.get_progress() == 1
    
    def test_save_process_status(self) -> None:
        assert True
    
    def test_reset_process(self)->None:
        manager = ProcessManager()
        process_id = 'abc'
        file_path = '/temp/'
        file_name = 'abc.txt'
        description = 'test'
        process = manager.create_process(process_id, file_path, file_name, description)
        manager.reset(process)
        process = manager.get_process_by_id(process_id)
        assert process.get_progress() == 0 and process.get_is_running() == False

    # check progress
    def test_check_progress(self) -> None:
        manager = ProcessManager()
        process_id = 'abc'
        progress = manager.check_progress(process_id)
        assert progress == 0

        


        
    

