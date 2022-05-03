from __future__ import annotations

from datetime import datetime
from typing import Any, List, NamedTuple, Tuple


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

    def load(self, loader: FileLoader) -> Any:
        pass


class FileLoader:
    """
    """

    def load_model(self, file: File) -> Model:
        pass

    def load_dataset(self, file: File) -> Dataset:
        pass

    def load_etl_code(self, file: File) -> EtlCode:
        pass


class LoadedFileBase(NamedTuple):

    name: str
    versions: List[File]
    thumbnail: str


class Model(LoadedFileBase):

    pass


class Dataset(LoadedFileBase):

    shape: Tuple[int, int]


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
        pass

    def add(self, file: File) -> None:
        self._file_dao.update(file)
