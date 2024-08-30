import os
from uuid import UUID

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.file_management import FilesService, Path
from src.cases.schemas import UniqueFieldsEnum
from src.utils import SingletonMeta
from src.infrastructure.database import BaseORMService

from .config import CasesConfig
from .models import Case


class CasesService(BaseORMService, metaclass=SingletonMeta):
    files_service = FilesService()

    def __init__(self):
        super().__init__(
            base_model=Case
        )

    async def get_by_unique_field_or_404(self, identifier: str, field: UniqueFieldsEnum, session: AsyncSession) -> Case | None:
        result = await self.get_by_unique_field(identifier, field, session)

        if result is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")

        return result

    async def get_by_unique_field(self, identifier: str, field: UniqueFieldsEnum, session: AsyncSession) -> Case | None:
        unique_field = getattr(self.BASE_MODEL, field)

        query = await session.execute(select(self.BASE_MODEL).where(unique_field == identifier))

        result = query.fetchone()

        return result[0] if result is not None else None

    async def save_content_file(self, case_id: UUID, file: UploadFile) -> Path:
        directory_path = os.path.join(CasesConfig.UPLOAD_DIRECTORY, case_id.hex)
        file_path = os.path.join(directory_path, f"{CasesConfig.CASES_CONTENT_FILE_NAME}.{CasesConfig.CASES_CONTENT_FILE_EXTENSION}")

        return await self.files_service.save_file(directory_path, file_path, file)

    async def save_preview_file(self, case_id: UUID, file: UploadFile) -> Path:
        directory_path = os.path.join(CasesConfig.UPLOAD_DIRECTORY, case_id.hex)
        file_path = os.path.join(directory_path, f"{CasesConfig.CASES_PREVIEW_FILE_NAME}.{CasesConfig.CASES_PREVIEW_FILE_EXTENSION}")

        return await self.files_service.save_file(directory_path, file_path, file)
