from fastapi import FastAPI

from api import router

tags_metadata = [
    {
        "name": "weather",
        "description": "Получения прогноза погоды",
    },
]


app = FastAPI(
    title="Weather forecast (Family doctor)",
    description="Сервис получения погоды",
    openapi_tags=tags_metadata,
)
app.include_router(
    router=router,
)
