import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "src.server:create_app", host="127.0.0.1", port=8003, factory=True
    )
