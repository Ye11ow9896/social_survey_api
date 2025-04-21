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
from src.core.domain.survey.dto import SurveyDTO
from src.core.domain.survey.service import SurveyService
from src.core.domain.auth.middleware import CheckAccessTokenMiddleware
from result import Err


class SurveyController(Controller):
    path = "/survey"
    tags = ("Survey endpoints",)
    middleware = [CheckAccessTokenMiddleware]

    @get(
        "/all",
        status_code=200,
        description="Получить список исследований",
    )
    @inject
    async def get_all(
        self,
        name: str | None,
        service: Injected[SurveyService],
        page_size: Annotated[
            int, Parameter(ge=1, le=1_000, query="pageSize")
        ] = 100,
        page: Annotated[int, Parameter(ge=1)] = 1,
    ) -> PaginationResponseSchema[SurveyDTO]:
        pagination_dto = PaginationDTO(
            page_size=page_size,
            page=page,
        )
        result = await service.get_all(pagination_dto, name)
        return PaginationResponseSchema(
            items=SurveyDTO.sqlalchemy_model_validate_list(result.items),
            has_next_page=result.has_next_page,
            count=result.count,
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
