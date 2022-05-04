from multiprocessing import Manager
from pathlib import Path
from pydoc import describe
from itsdangerous import NoneAlgorithm
import pytest
from model_manager.firebase_daos import UploadProcessDao, FileDao
from model_manager.process_manager import ProcessManager
from model_manager.process import UploadProcess
from werkzeug.wsgi import LimitedStream

import os
from datetime import datetime

@pytest.fixture()
def manager():
    dao = UploadProcessDao()
    process_waiting = UploadProcess('waiting', '/temp/', 'waiting process.txt', 'description')
    process_waiting.set_is_running(False)
    process_waiting.set_is_done(False)
    process_waiting.set_progress(0)
    process_running = UploadProcess('running', '/temp/', 'running process.txt', 'description')
    process_running.set_is_running(True)
    process_running.set_is_done(False)
    process_running.set_progress(0.5)
    process_finish = UploadProcess('finish', '/temp/', 'finish process.txt', 'description')
    process_finish.set_is_running(False)
    process_finish.set_is_done(True)
    process_finish.set_progress(1)
    dao.add(process_waiting)
    dao.add(process_running)
    dao.add(process_finish)
    yield ProcessManager()
    dao.delete(process_waiting)
    dao.delete(process_running)
    dao.delete(process_finish)


class TestProcessManager:

    def test_load_waiting_process(self, manager) -> None:
        processs_id_list = manager.load_waiting_process_id()
        if(processs_id_list != None and len(processs_id_list) > 0):
            process = manager.get_process_by_id('waiting')
            assert process.get_is_running() == False and process.get_is_done() == False
        
        
    def test_load_finish_process(self, manager) -> None:
        manager = ProcessManager()
        processs_id_list = manager.load_waiting_process_id()
        if(processs_id_list != None and len(processs_id_list[0]) > 0):
            process = manager.get_process_by_id('finish')
            assert process.get_is_done() == True
    
    def test_load_running_process(self, manager) -> None:
        processs_id_list = manager.load_waiting_process_id()
        if(processs_id_list != None and len(processs_id_list) > 0):
            process = manager.get_process_by_id('running')
            assert process.get_is_running() == True and process.get_is_done() == False
    
    def test_check_process_in_queue_not_exist_case(self) -> None:
        manager = ProcessManager()
        process_id = 'not exist'
        assert not manager.check_process_in_queue(process_id, [])

    def test_get_process_by_id(self, manager) -> None:
        process_id = 'waiting'
        process = manager.get_process_by_id(process_id)
        assert process.get_process_id() == process_id
    
    # upload_file api test
    def test_upload_file_request(self, manager) -> None:
        dao = UploadProcessDao()
        old_list = manager.load_waiting_process_id()
        file_name = 'abc.txt'
        description = "upload_file_request"
        process_id =  manager.upload_file_request(file_name, description)
        process = manager.get_process_by_id(process_id)
        new_list = manager.load_waiting_process_id()
        dao.delete(process)
        assert len(new_list) - len(old_list) == 1 and process.get_process_id() == process_id

    def test_check_storage_has_space(self) -> None:
        manager = ProcessManager()
        assert manager.check_storage_has_space() > 0

    #transport file api test 
    def test_transport_file(self, manager) -> None:
        dao = UploadProcessDao()
        path = './data/'
        file_path = './data/temp/'
        file_name = 'abc.txt'
        description = 'test_transport_file'
        chunk_size = 3
        file_size = os.stat(path + file_name).st_size
        process_id = manager.upload_file_request(file_name, description)
        process = manager.get_process_by_id(process_id)
        with open(path + file_name, "rb") as file:
            limited_stream = LimitedStream(file, file_size)
            manager.transport_file(process, limited_stream, file_size)
        dao.delete(process)
        with open(file_path + file_name, "rb") as file:
            assert file.readline().decode("utf-8") == 'abc\r\n'
        fdao = FileDao()
        fdao.delete(file_name)
    
    def test_reset_process(self, manager)->None:
        process = manager.get_process_by_id('running')
        manager.reset_process(process)
        process = manager.get_process_by_id('running')
        assert process.get_progress() == 0 and process.get_is_running() == False

    # check progress
    def test_check_progress(self, manager) -> None:
        process_id = 'running'
        progress = manager.check_progress(process_id)
        assert progress == str(0.5)

        


        
    

