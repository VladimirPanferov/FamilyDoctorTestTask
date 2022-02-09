from fastapi import FastAPI


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
