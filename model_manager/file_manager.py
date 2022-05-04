from __future__ import annotations

from abc import abstractmethod
from datetime import datetime
from importlib.abc import Loader
from typing import Any, List, NamedTuple, Tuple

from pandas import DataFrame, read_csv


class File(NamedTuple):
    """Maintain the storing information of file.
    """

    name: str
    type: str
    description: str
    path: str
    uploader: str
    upload_time: datetime
    last_used_time: datetime

    def load(self, loader: FileLoader) -> LoadedFileBase:
        if self.type == 'dataset':
            return loader.load_dataset(self)
        else:
            raise NotImplementedError('to be update.')


class FileLoader:

    def load_model(self, file: File) -> Model:
        pass

    def load_dataset(self, file: File) -> Dataset:
        if file.path.endswith('.csv'):
            dataframe = read_csv(file.path)
        else:
            raise ValueError(f'Invalid file format ({file.path=})')

        return Dataset(
            name=file.name,
            dataframe=dataframe,
        )

    def load_etl_code(self, file: File) -> EtlCode:
        pass


class LoadedFileBase:

    def __init__(self,
                 name: str,
                 type: str,
                 versions: List[File] = None) -> None:
        self._name = name
        self._type = type
        self._versions = versions if versions is not None else []

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> str:
        return self._type

    @property
    def versions(self) -> List[File]:
        return self._version

    @property
    @abstractmethod
    def thumbnail(self) -> str:
        pass


class Model(LoadedFileBase):

    pass


class Dataset(LoadedFileBase):

    def __init__(self,
                 name: str,
                 dataframe: DataFrame,
                 versions: List[File] = None) -> None:
        super().__init__(name=name, type='dataset', versions=versions)

        self._dataframe = dataframe

    @property
    def dataframe(self) -> DataFrame:
        return self._dataframe

    @property
    def thumbnail(self) -> str:
        return str(self._dataframe.head())


class EtlCode(LoadedFileBase):

    language: str


class FileManager:

    def __init__(self) -> None:
        # TODO: solve circular import
        from model_manager.firebase_daos import FileDao
        self._file_dao = FileDao()

        self._files = None

    @property
    def files(self) -> List[File]:
        if self._files is None:
            self._files = self._file_dao.get_all()

        return self._files

    def view_loaded_file(self, name: str) -> LoadedFileBase:
        file_names = [file.name for file in self.files]

        if name not in file_names:
            raise ValueError(f'file dose not exists ({name=})')

        file = self.files[file_names.index(name)]
        return file.load(FileLoader())

    def add(self, file: File) -> None:
        # TODO: update self._files
        self._file_dao.update(file)
