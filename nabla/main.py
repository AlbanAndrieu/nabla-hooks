from typing import Dict

from nabla import logger
from nabla.api import ping, v1

# from citation import logger
from citation.api import api

# from citation.infrastructure.crud_exceptions import CrudError, NotFoundInJM

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

logger.info("Creating API")
app = FastAPI(
    title="Nabla V1",
    version="0.0.1",
)

origins = ["http://localhost", "http://localhost:8080", "http://localhost:5173", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)


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


@app.on_event("startup")
async def startup():
    # await database.connect()
    Instrumentator().instrument(app).expose(app)
    FastAPIInstrumentor.instrument_app(app)


# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()


@app.get("/health")
def get_status() -> Dict[str, str]:
    """Healthcheck endpoint."""
    return {"status": "pass"}


app.include_router(ping.router)
app.include_router(v1.router)
app.include_router(api.router)
# app.include_router(notes.router, prefix="/notes", tags=["notes"])
