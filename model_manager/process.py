from werkzeug.wsgi import LimitedStream
class Process():

    def __init__(self, process_id, file_name, description, file_path):
        self.process_id: str = process_id
        self.file_name: str = file_name
        self.description: str = description
        self.file_path: str = file_path
        self.file_stream: LimitedStream
        self.progress: int = 0
        self.is_done: bool = False
    
    def get_process_id(self):
        return self.process_id
    
    def set_stream(self, file_stream: LimitedStream):
        self.file_stream = file_stream

    def get_stream(self) -> LimitedStream:
        return self.file_stream

    def get_progress(self) -> int:
        pass