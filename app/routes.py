from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.db import InMemoryDB
from app.models import Document, DocumentIdList

THRESHOLD = 75

router = APIRouter()
db = InMemoryDB(partial_ratio_threshold=THRESHOLD)


@router.post("/documents/{document_id}")
def post_document(document_id: str, request_payload: Document):
    db[document_id] = request_payload
    return JSONResponse(
        status_code=200,
        content={"status": "document added", "document_id": document_id},
    )


@router.delete("/documents/{document_id}")
def delete_document(document_id: str):
    if document_id not in db:
        raise HTTPException(
            status_code=404,
            detail={"error": "Document Not Found", "document_id": document_id},
        )
    db.delete_document(document_id)
    return JSONResponse(
        status_code=200, content={"status": "deleted", "document_id": document_id}
    )


@router.get("/documents/deleted", response_model=DocumentIdList)
def delete_document():
    return DocumentIdList(
        status=200, total=len(db.get_deleted_uids()), document_ids=db.get_deleted_uids()
    )


@router.get("/search")
def search_by_keyword(keyword: str, fuzzy: str = "off"):
    doc_ids = db.get_doc_ids_by_keyword(keyword, fuzzy=True if fuzzy == "on" else False)
    return DocumentIdList(status=200, total=len(doc_ids), document_ids=doc_ids)
