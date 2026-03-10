from fastapi import FastAPI

from app.api.inbound import router

app = FastAPI(
    title="{{ service_name }}",
    description="{{ service_description }}",
)

app.include_router(router)
