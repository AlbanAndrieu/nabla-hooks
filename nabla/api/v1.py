from fastapi import APIRouter
from fastapi import HTTPException, status
from starlette.responses import JSONResponse

# from datetime import date, timedelta

from opentelemetry import trace
from opentelemetry.trace.status import Status, StatusCode

import asyncio
import requests
import logging
import random

random.seed(54321)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter(prefix="/v1")

# See https://signoz.io/blog/opentelemetry-fastapi/
# https://github.com/SigNoz/sample-fastAPI-app/blob/main/app/main.py


@router.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    if item_id % 2 == 0:
        # mock io - wait for x seconds
        seconds = random.uniform(0, 3)
        await asyncio.sleep(seconds)
    return {"item_id": item_id, "q": q}


@router.get("/invalid")
async def invalid():
    raise ValueError("Invalid ")


@router.get("/exception")
async def exception():
    try:
        raise ValueError("sadness")
    except Exception as ex:
        logger.error(ex, exc_info=True)
        span = trace.get_current_span()

        # generate random number
        seconds = random.uniform(0, 30)

        # record_exception converts the exception into a span event.
        exception = IOError("Failed at " + str(seconds))
        span.record_exception(exception)
        span.set_attributes({"est": True})
        # Update the span status to failed.
        span.set_status(Status(StatusCode.ERROR, "internal error"))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Got sadness") from ex


@router.get("/external-api")
def external_api():
    seconds = random.uniform(0, 3)
    response = requests.get(f"https://httpbin.org/delay/{seconds}")
    response.close()
    return "ok"


@router.get("/ping")
async def pong():
    """
    Healthcheck endpoint.
    """
    return JSONResponse({"ping": "pong v1!"})
