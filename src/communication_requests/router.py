from fastapi import (
    APIRouter,
    Request,
    Response,
)
from starlette import status
from fastapi_restful.cbv import cbv

from src.infrastructure.rate_limit import limiter

from .schemas import CreateCommunicationRequest
from .service import CommunicationRequestsService


router = APIRouter(prefix="/communication-requests", tags=["communication-requests"])


@cbv(router)
class CommunicationRequestsView:
    service = CommunicationRequestsService()

    @router.post("/", response_model=None)
    @limiter.limit("3/minute")
    async def create_post(self, data: CreateCommunicationRequest, request: Request):
        await self.service.send_new_communication_request_message_to_admins(data.c)
        return Response(status=status.HTTP_200_OK)
