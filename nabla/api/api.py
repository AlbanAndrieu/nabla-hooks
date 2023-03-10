from datetime import date, timedelta

from fastapi import APIRouter
from starlette.responses import JSONResponse

# from citation.api.api_models import XMLResponse, PlainResponse
# from citation.documents_ids_fetcher import fetch_documents_ids
# from citation.predict import predict_citations_db
# from citation.utils import DocumentType

router = APIRouter(prefix="/v1")


# @router.get("/request/newsletter_ids/{document_type}")
# async def request_newsletter_ids(
#     document_type: DocumentType,
# ):
#     found_ids = await fetch_documents_ids(
#         document_type=document_type,
#         start_date=date.today() - timedelta(days=7),
#         end_date=date.today(),
#     )
#     return PlainResponse(found_ids)


# @router.get("/detection/{document_type}/{document_id}/{document_locale}")
# async def detect_citations_document(
#     document_type: DocumentType,
#     document_id: int,
#     document_locale: str = "en",
# ):
#     citations = await predict_citations_db(
#         document_type=document_type,
#         document_id=document_id,
#         document_locale=document_locale,
#     )
#     return XMLResponse(citations)


@router.get("/ping")
async def pong():
    """
    Healthcheck endpoint.
    """
    return JSONResponse({"ping": "pong"})
