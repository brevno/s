from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from server.config import settings
from server.views import router

def configure_app(app: FastAPI) -> FastAPI:
    app.include_router(router)
    _configure_cors(app)
    return app

def _configure_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
app = FastAPI()
configure_app(app)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
