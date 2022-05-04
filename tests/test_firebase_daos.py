from datetime import datetime

import pytest
from model_manager.file_manager import File
from model_manager.firebase_daos import FileDao


class TestFileDao:

    @staticmethod
    def assert_equal(lhs: File, rhs: File) -> bool:
        assert lhs.name == rhs.name
        assert lhs.type == rhs.type
        assert lhs.description == rhs.description
        assert lhs.path == rhs.path
        assert lhs.uploader == rhs.uploader
        assert lhs.upload_time.timestamp() == pytest.approx(
            rhs.upload_time.timestamp())
        assert lhs.last_used_time.timestamp() == pytest.approx(
            rhs.last_used_time.timestamp())

    def test_update_and_getters(self) -> None:
        dao = FileDao()

        with pytest.raises(ValueError):
            # TODO: make sure the file is not exist.
            dao.get('not-exist-test-file')

        file = File(
            name='test-file',
            type='test',
            description='test-file',
            path='/',
            uploader='test',
            upload_time=datetime(2022, 5, 3, 2, 45),
            last_used_time=datetime(2022, 5, 3, 2, 46, 7),
        )
        dao.update(file)
        self.assert_equal(dao.get('test-file'), file)

        file2 = File(
            name='test-file',
            type='test',
            description='test-file-updated',
            path='/',
            uploader='test',
            upload_time=datetime.now(),
            last_used_time=datetime.now(),
        )
        dao.update(file2)
        self.assert_equal(dao.get('test-file'), file2)
