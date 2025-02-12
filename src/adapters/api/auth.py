from litestar import get, post
from litestar.controller import Controller

from core.domain.auth.dto import AuthDTO
from aioinject import Injected
from aioinject.ext.fastapi import inject
from core.domain.user.repository import UserRepository


class AuthController(Controller):
    path = "/auth"
    tags = ("Auth group",)

    @post("/authorization", dto=AuthDTO)
    @inject
    async def get_token(self, repo: Injected[UserRepository]) -> str:
        await repo.create("pppp")
        return "Hello, world!"

    @get("/books/{book_id:int}")
    async def get_book(self, book_id: int) -> dict[str, int]:
        return {"book_id": book_id}
