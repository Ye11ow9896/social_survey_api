from litestar import get, post
from litestar.controller import Controller

from src.core.auth.dto import AuthDTO, AuthDataclass


class AuthController(Controller):
    path = "/auth"
    tags = ("Auth group",)

    @post("/authorization", dto=AuthDTO)
    async def get_token(self, data: AuthDataclass) -> str:
        return "Hello, world!"

    @get("/books/{book_id:int}")
    async def get_book(self, book_id: int) -> dict[str, int]:
        return {"book_id": book_id}
