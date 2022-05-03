import os
from datetime import datetime

import pandas as pd
from model_manager.file_manager import File, FileLoader, FileManager


class TestFileLoader:

    def test_load_csv_dataset(self) -> None:
        dataframe = pd.DataFrame({
            'a': [1, 2, 3],
            'b': [4, 5, 6],
            'c': [7, 8, 9],
        })
        dataframe.to_csv('./tests/test-dataframe.csv', index=False)

        file = File(
            name='test-csv-file',
            type='dataset',
            description='test-csv-file',
            path='./tests/test-dataframe.csv',
            uploader='test',
            upload_time=datetime.now(),
            last_used_time=datetime.now(),
        )
        result = FileLoader().load_dataset(file)
        assert result.dataframe.equals(dataframe)

        # TODO: make execute even when exceptions issueed before
        os.remove('./tests/test-dataframe.csv')


class TestFile:

    def test_load_csv_dataset(self) -> None:

        pass


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

        file_manager.add(file1)
        file_manager.add(file2)

        assert 'test-file-1' in [file.name for file in file_manager.files]
        assert 'test-file-2' in [file.name for file in file_manager.files]

        # TODO: clean update files
