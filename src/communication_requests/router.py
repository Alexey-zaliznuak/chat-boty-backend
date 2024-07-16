from fastapi import (
    APIRouter,
    Request,
    Response,
)
from fastapi_restful.cbv import cbv

from src.infrastructure.rate_limit import limiter

from .schemas import CreateCommunicationRequest
from .service import CommunicationRequestsService


router = APIRouter(prefix="/communication-requests", tags=["communication-requests"])


@cbv(router)
class CommunicationRequestsView:
    service = CommunicationRequestsService()

    @router.post("/", response_model=None)
    @limiter.limit("1/minute")
    async def create_post(self, data: CreateCommunicationRequest, request: Request):
        await self.telegram_service.notify_in_admin_group(
            contact_type=data.contact_type,
            contact=data.value
        )

        return Response()
