import requests
class process():

    def __init__(self, process_id, file_name, file_path):
        self.process_id: str = process_id
        self.file_name: str = file_name
        self.file_path: str = file_path
        self.file_stream: requests.Response
        self.progress: int = 0
        self.is_done: bool = False
    
    def set_stream(response):
        self.file_stream = response

    def get_stream() -> requests.Response:
        return self.file_stream

    def get_progress() -> int:
        pass