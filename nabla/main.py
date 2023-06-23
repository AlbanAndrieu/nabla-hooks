import logging
import os
import time
from typing import Dict

from fastapi import FastAPI

# from nabla import logger
from nabla.api import ping, v1
from nabla.utils import PrometheusMiddleware, metrics, setting_otlp

# from prometheus_fastapi_instrumentator import Instrumentator

# from citation import API
# from citation.api import api

# from citation.infrastructure.crud_exceptions import CrudError, NotFoundInJM




APP_NAME = os.environ.get("APP_NAME", "nabla-hooks")
OTLP_GRPC_ENDPOINT = os.environ.get(
    "OTLP_GRPC_ENDPOINT", "http://grpc.jaeger-collector-grpc.service.gra.dev.consul"
)
# http://grpc.jaeger-collector-grpc.service.gra.dev.consul
# http://jaeger-collector-grpc.service.gra.dev.consul:14250
# http://otel-collector.service.gra.dev.consul:4317
# http://otel-collector.service.gra.dev.consul:9411/api/v2/spans

# logger.info("Creating API")
logging.info("Creating API")
app = FastAPI(
    title="Nabla V1",
    version="0.0.1",
)

# origins = ["http://localhost", "http://localhost:8080", "http://localhost:5173", "*"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["DELETE", "GET", "POST", "PUT"],
#     allow_headers=["*"],
# )

# Setting metrics middleware
app.add_middleware(
    PrometheusMiddleware,
    app_name=APP_NAME,
)

app.add_route("/metrics", metrics)

# Setting OpenTelemetry exporter
setting_otlp(app, APP_NAME, OTLP_GRPC_ENDPOINT)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


# @app.exception_handler(NotFoundInJM)
# async def not_found_jm_handler(request: Request, exc: NotFoundInJM):
#    return JSONResponse(
#        status_code=404,
#        content={"message": str(exc)},
#    )
#
#
# @app.exception_handler(CrudError)
# async def crud_error_handler(request: Request, exc: CrudError):
#    logger.error("Error while querying the DB")
#    logger.exception(exc)
#    return JSONResponse(
#        status_code=500,
#        content={"message": f"Error while querying the DB: {exc}"},
#    )
#
#
# @app.exception_handler(Exception)
# async def exception_handler(request: Request, exc: Exception):
#    logger.error("Unexpected error")
#    logger.exception(exc)
#    return JSONResponse(
#        status_code=500,
#        content={"message": f"Unexpected error: {exc}"},
#    )
@app.get("/io_task")
async def io_task():
    time.sleep(1)
    logging.error("io task")
    return "IO bound task finish!"


@app.get("/cpu_task")
async def cpu_task():
    for i in range(1000):
        i * i * i
    logging.error("cpu task")
    return "CPU bound task finish!"


@app.on_event("startup")
async def startup():
    # await database.connect()
    ## Instrumentator().instrument(app).expose(app)
    # FastAPIInstrumentor.instrument_app(app)
    logging.info("API is ready")


# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()


@app.get("/health")
def get_status() -> Dict[str, str]:
    """Healthcheck endpoint."""
    return {"status": "pass"}


app.include_router(ping.router)
app.include_router(v1.router)
# app.include_router(api.router)
# app.include_router(notes.router, prefix="/notes", tags=["notes"])
