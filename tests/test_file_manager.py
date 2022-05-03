from datetime import datetime
from model_manager.file_manager import FileManager, File


class TestFileManager:

    def test_add_file(self) -> None:
        file_manager = FileManager()

        file1 = File(
            name='test-file-1',
            type='dataset',
            description='test-file-1',
            path='./test-file-1.csv',
            uploader='test',
            upload_time=datetime(2022, 5, 3, 12, 43),
            last_used_time=datetime(2022, 5, 3, 12, 44),
        )
        file2 = File(
            name='test-file-2',
            type='dataset',
            description='test-file-2',
            path='./test-file-2.csv',
            uploader='test',
            upload_time=datetime(2022, 5, 3, 11, 43),
            last_used_time=datetime(2022, 5, 3, 11, 44),
        )

        assert len(file_manager.files) == 0

        file_manager.add(file1)
        assert len(file_manager.files) == 1
        assert file_manager.files[0] == file1

        file_manager.add(file2)
        assert len(file_manager.files) == 2
        assert file_manager.files[1] == file2
