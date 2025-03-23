from http import HTTPStatus
from inspect import Parameter
from typing import Annotated, Any
from result import Err

from litestar import Response, get, post
from litestar.controller import Controller
from litestar.params import Parameter
from aioinject import Injected
from aioinject.ext.litestar import inject

from src.lib.paginator import PaginationDTO, PaginationResultDTO
from src.adapters.api.schema import APIDetailSchema
from src.adapters.api.survey.schema import SurveyCreateSchema
from src.adapters.api.exceptions import ObjectNotFoundHTTPError
from src.core.domain.survey.dto import SurveyDTO
from src.core.domain.survey.service import SurveyService
from src.core.domain.auth.middleware import CheckAccessTokenMiddleware


class SurveyController(Controller):
    path = "/survey"
    tags = ("Survey endpoints",)
    middleware = [CheckAccessTokenMiddleware]

    @get("/all", status_code=200)
    @inject
    async def get_all(
        self,
        name: str | None,
        service: Injected[SurveyService],
        page_size: Annotated[
            int, Parameter(ge=1, le=1_000, query="pageSize")
        ] = 100,
        page: Annotated[int, Parameter(ge=1)] = 1,
    ) -> PaginationResultDTO[SurveyDTO]:
        pagination_dto = PaginationDTO(
            page_size=page_size,
            page=page,
        )
        result = await service.get_all(
            pagination_dto, name
        )
        if isinstance(result, Err):
            raise ObjectNotFoundHTTPError(message=result.err_value.message)
        return result.ok()

    @post("/create", status_code=200)
    @inject
    async def create(
        self,
        data: SurveyCreateSchema,
        service: Injected[SurveyService],
    ) -> Response[Any]:
        dto = data.to_dto()
        await service.create(dto)
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
