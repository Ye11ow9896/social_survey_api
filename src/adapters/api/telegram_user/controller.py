from http import HTTPStatus
from typing import Any, Annotated

from adapters.api.schema import APIDetailSchema
from adapters.api.telegram_user.dto import TelegramUserFilterDTO
from adapters.api.telegram_user.schema import TelegramUserCreateSchema
from core.domain.auth.middleware import CheckAccessTokenMiddleware
from core.domain.user.dto import TelegramUserDTO
from core.domain.user.service import TelegramUserService
from litestar import Response
from sqla_filter import or_unset
from litestar import post, get
from litestar.params import Parameter
from litestar.controller import Controller
from aioinject import Injected
from aioinject.ext.litestar import inject
from database.enums import RoleCodeEnum
from lib.paginator import PaginationResultDTO, PaginationDTO


class TelegramUserController(Controller):
    path = "/telegram-user"
    tags = ("Telegram user endpoints",)
    middleware = [CheckAccessTokenMiddleware]

    @post("/create", status_code=200)
    @inject
    async def create(
        self,
        role: RoleCodeEnum,
        data: TelegramUserCreateSchema,
        service: Injected[TelegramUserService],
    ) -> Response[Any]:
        dto = data.to_dto(role=role)
        await service.create(dto)
        return Response(
            content={
                "detail": APIDetailSchema(
                    status_code=HTTPStatus.OK,
                    code="tg_user_create_success",
                    message="Пользователь создан успешно",
                )
            },
            status_code=HTTPStatus.OK,
        )

    @get("/all", status_code=200)
    @inject
    async def get_all(
        self,
        tg_id: Annotated[int | None, Parameter(query="tgId")],
        is_bot: Annotated[bool | None, Parameter(query="isBot")],
        service: Injected[TelegramUserService],
        page_size: Annotated[
            int, Parameter(ge=1, le=1_000, query="pageSize")
        ] = 100,
        page: Annotated[int, Parameter(ge=1)] = 1,
    ) -> PaginationResultDTO[TelegramUserDTO]:
        filter_dto = TelegramUserFilterDTO(
            tg_id=or_unset(tg_id),
            is_bot=or_unset(is_bot),
        )
        pagination_dto = PaginationDTO(
            page_size=page_size,
            page=page,
        )
        return await service.get_all(filter_dto, pagination=pagination_dto)
