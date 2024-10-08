from fastapi import UploadFile
from os import makedirs, remove

from src.utils import SingletonMeta


type Path = str


class FilesService(metaclass=SingletonMeta):
    async def save_file(self, directory_path: str, file_path: str, file: UploadFile | bytes) -> Path:
        content = await self.__get_file_content(file)

        makedirs(directory_path, exist_ok=True)

        with open(file_path, "wb") as buffer:
            buffer.write(content)

        return file_path


    def delete_file(self, file: str, *, not_exists_ok: bool = True):
        try:
            remove(file)

        except FileNotFoundError as e:
            if not not_exists_ok:
                raise e

    # TODO: refactor
    async def __get_file_content(self, file) -> bytes:
        if isinstance(file, bytes):
            return file

        return await file.read()
