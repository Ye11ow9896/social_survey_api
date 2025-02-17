from http import HTTPStatus
from typing import Any

from adapters.api.schema import APIDetailSchema
from adapters.api.telegram_user.schema import TelegramUserCreateSchema
from core.domain.user.service import TelegramUserService
from litestar import Response

from litestar import post
from litestar.controller import Controller
from aioinject import Injected
from aioinject.ext.fastapi import inject

from database.enums import RoleCodeEnum


class TelegramUserController(Controller):
    path = "/telegram-user"
    tags = ("Telegram user endpoints",)

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
