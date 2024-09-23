from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Response,
    status
)
from fastapi_restful.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.auth import admin_access
from src.database import get_async_session
from src.infrastructure.route.pagination import (
    PaginatedResponse,
    PaginationParams,
    get_pagination_params
)
from src.infrastructure.rate_limit import limiter

from .config import CasesConfig as Config
from .dependencies import get_cases_filter_params, validate_case
from .models import Case
from .filters import CaseFilterParams
from .schemas import (
    CreateCase,
    GetCaseResponse,
    UpdateCase,
)
from .service import CasesService


router = APIRouter(prefix="/cases", tags=["cases"])


@cbv(router)
class CasesView:
    service = CasesService()
    session: AsyncSession = Depends(get_async_session)

    @router.get("/", response_model=PaginatedResponse[GetCaseResponse])
    @limiter.limit("10/minute")
    async def get_all(
        self,
        request: Request,
        pagination: PaginationParams = Depends(get_pagination_params),
        filters: CaseFilterParams = Depends(get_cases_filter_params)
    ):
        return await self.service.get_many_with_pagination(
            pagination,
            self.session,
            where=filters,
        )

    @router.get("/{identifier}/", response_model=GetCaseResponse)
    @limiter.limit("10/minute")
    async def get(
        self,
        request: Request,
        case: Case = Depends(validate_case)
    ):
        return case

    @router.get("/{identifier}/content")
    @limiter.limit("10/minute")
    async def get_content_file(
        self,
        request: Request,
        case: Case = Depends(validate_case)
    ) -> str | None:
        return case.content

    @router.post("/", response_model=GetCaseResponse)
    @admin_access()
    async def create(self, data: CreateCase, request: Request):
        slug = await Case.generate_slug(data.title, self.session)

        new_case = Case(**data.model_dump(), slug=slug)

        await self.service.save_and_refresh(new_case, self.session)

        if not new_case:
            raise HTTPException(status.HTTP_409_CONFLICT, "Failed to create case")

        return new_case

    @router.patch("/{identifier}", response_model=GetCaseResponse)
    @admin_access()
    async def update(
        self,
        data: UpdateCase,
        request: Request,
        case: Case = Depends(validate_case)
    ):
        await self.service.update_instance_fields(
            case,
            data=data.model_dump(exclude_unset=True),
            session=self.session,
            save=True,
        )
        return case

    @router.delete("/{identifier}", response_model=None)
    @admin_access()
    async def delete(
        self,
        request: Request,
        case: Case = Depends(validate_case),
    ):
        await self.service.delete_by_id(case.id, self.session)

        return Response(status_code=status.HTTP_204_NO_CONTENT)
