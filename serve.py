import uvicorn

from typing import Dict

from nabla import logger
from nabla.api import api

# from citation import logger
# from citation.api import api
# from citation.infrastructure.crud_exceptions import CrudError, NotFoundInJM

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.requests import Request
from starlette.responses import JSONResponse

logger.info("Creating API")
app = FastAPI(
    title="Nabla V1",
    version="0.0.1",
)
app.include_router(api.router)


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
    Instrumentator().instrument(app).expose(app)


@app.get("/health")
def get_status() -> Dict[str, str]:
    """Healthcheck endpoint."""
    return {"status": "pass"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_config=None)
