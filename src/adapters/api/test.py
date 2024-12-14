from litestar import get, post
from litestar.controller import Controller


class TestController(Controller):
    path = "/test"
    tags = ("TEST GROUP",)

    @post("/")
    async def index(self) -> str:
        return "Hello, world!"

    @get("/books/{book_id:int}")
    async def get_book(self, book_id: int) -> dict[str, int]:
        return {"book_id": book_id}
