from http import HTTPStatus
from typing import Annotated, Any

from litestar import Response, get, post
from litestar.controller import Controller
from litestar.params import Parameter
from aioinject import Injected
from aioinject.ext.litestar import inject

from src.adapters.api.exceptions import (
    ObjectNotFoundHTTPError,
    PermissionDeniedForRoleHTTPError,
)
from src.core.domain.survey.exceptions import PermissionDeniedForRoleError
from src.core.exceptions import ObjectNotFoundError
from src.lib.paginator import PaginationDTO
from src.adapters.api.schema import APIDetailSchema, PaginationResponseSchema
from src.adapters.api.survey.schema import SurveyCreateSchema
from src.core.domain.survey.dto import AssingSurveyDTO, SurveyDTO
from src.core.domain.survey.service import SurveyService
from src.core.domain.auth.middleware import CheckAccessTokenMiddleware
from result import Err


class SurveyController(Controller):
    path = "/survey"
    tags = ("Survey endpoints",)
    middleware = [CheckAccessTokenMiddleware]

    @get(
        "/assingned/all",
        status_code=200,
        description="Получить список исследований",
    )
    @inject
    async def get_survey_assign_list(
        self,
        service: Injected[SurveyService],
        tg_id: Annotated[int | None, Parameter(query="tgId")] = None,
        name: str | None = None,
        page_size: Annotated[
            int, Parameter(ge=1, le=1_000, query="pageSize")
        ] = 100,
        page: Annotated[int, Parameter(ge=1)] = 1,
    ) -> PaginationResponseSchema[SurveyDTO]:
        pagination_dto = PaginationDTO(
            page_size=page_size,
            page=page,
        )
        result = await service.get_assign_list(
            pagination_dto,
            dto=AssingSurveyDTO(
                tg_id=tg_id,
                name=name,
            ) 
        )
        return PaginationResponseSchema[SurveyDTO].model_validate(
            result
        )

    @post(
        "/create",
        status_code=200,
        description="Создать исследование",
    )
    @inject
    async def create(
        self,
        data: SurveyCreateSchema,
        service: Injected[SurveyService],
    ) -> Response[Any]:
        dto = data.to_dto()
        result = await service.create(dto)
        if isinstance(result, Err):
            match exc := result.err_value:
                case ObjectNotFoundError():
                    raise ObjectNotFoundHTTPError(message=exc.message)
                case PermissionDeniedForRoleError():
                    raise PermissionDeniedForRoleHTTPError(message=exc.message)
        return Response(
            content={
                "detail": APIDetailSchema(
                    status_code=HTTPStatus.OK,
                    code="survey_create_success",
                    message="Опрос создан успешно",
                )
            },
            status_code=HTTPStatus.OK,
        )
