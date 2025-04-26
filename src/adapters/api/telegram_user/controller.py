from http import HTTPStatus
from typing import Any, Annotated
from uuid import UUID
from result import Err
from litestar import Response
from litestar import post, get
from litestar.params import Parameter
from litestar.controller import Controller

from src.adapters.api.schema import APIDetailSchema, PaginationResponseSchema
from src.adapters.api.exceptions import (
    ObjectNotFoundHTTPError,
    ObjectAlreadyExistsHTTPError,
)
from src.adapters.api.telegram_user.schema import (
    TelegramUserCreateSchema,
    TelegramUserRoleSchema,
)
from src.core.domain.auth.middleware import CheckAccessTokenMiddleware
from src.core.domain.role.service import RoleService
from src.core.domain.user.dto import TelegramUserDTO
from src.core.domain.user.service import TelegramUserService

from aioinject import Injected
from aioinject.ext.litestar import inject
from src.database.enums import RoleCodeEnum
from src.lib.paginator import PaginationDTO


class TelegramUserController(Controller):
    path = "/telegram-user"
    tags = ("Telegram user endpoints",)
    middleware = [CheckAccessTokenMiddleware]

    @post(
        "/create",
        status_code=200,
        description="Добавить нового пользователя",
    )
    @inject
    async def create(
        self,
        role: RoleCodeEnum,
        data: TelegramUserCreateSchema,
        service: Injected[TelegramUserService],
    ) -> Response[Any]:
        dto = data.to_dto(role=role)
        user = await service.create(dto)
        if isinstance(user, Err):
            raise ObjectAlreadyExistsHTTPError(message=user.err_value.message)
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

    @get(
        "/all",
        status_code=200,
        description="Вернуть список пользователей",
    )
    @inject
    async def get_all(
        self,
        tg_id: Annotated[int | None, Parameter(query="tgId")],
        is_bot: Annotated[bool | None, Parameter(query="isBot")],
        role: RoleCodeEnum | None,
        service: Injected[TelegramUserService],
        page_size: Annotated[
            int, Parameter(ge=1, le=1_000, query="pageSize")
        ] = 100,
        page: Annotated[int, Parameter(ge=1)] = 1,
    ) -> PaginationResponseSchema[TelegramUserDTO]:
        pagination_dto = PaginationDTO(
            page_size=page_size,
            page=page,
        )
        result = await service.get_all(
            pagination_dto, tg_id=tg_id, is_bot=is_bot, role=role
        )
        return PaginationResponseSchema(
            items=TelegramUserDTO.sqlalchemy_model_validate_list(result.items),
            has_next_page=result.has_next_page,
            count=result.count,
        )

    @get(
        "/role/{tg_id:int}",
        status_code=200,
        description="Получить роль пользователя",
    )
    @inject
    async def get_user_role(
        self,
        tg_id: int,
        service: Injected[RoleService],
    ) -> TelegramUserRoleSchema:
        result = await service.get_role_by_user(tg_id)
        if isinstance(result, Err):
            raise ObjectNotFoundHTTPError(message=result.err_value.message)
        return TelegramUserRoleSchema.model_validate(result.ok_value)

    @post("/assign-questionnaire/{tg_id:int}")
    @inject
    async def user_questionnaire_relations(
        self,
        tg_id: int,
        questionnaire_id: UUID,
        service: Injected[TelegramUserService],
    ) -> Response[Any]:
        result = await service.appoint_questionnaire_to_user(
            tg_id, questionnaire_id
        )
        if isinstance(result, Err):
            raise ObjectNotFoundHTTPError(message=result.err_value.message)
        return Response(
            content={
                "detail": APIDetailSchema(
                    status_code=HTTPStatus.OK,
                    code="telegram_respondent_questionnaire_create_success",
                    message=f"Анкета {questionnaire_id} успешно назначена на респондента {tg_id}",
                )
            },
            status_code=HTTPStatus.OK,
        )
