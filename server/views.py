import http.client
from datetime import datetime, timedelta

from fastapi import Depends, APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from server.db import Link, db_session_default_params
from server.hash import compact_hash
from server.models import URLInput, CreatedResponse


router = APIRouter()


@router.post("/create", response_model=CreatedResponse)
def create_short_url(url_input: URLInput, request: Request, db: Session = Depends(db_session_default_params)):
    url = str(url_input.url)

    link = db.query(Link).filter_by(url=url).first()
    if not link:
        link = Link(url=url, hash=compact_hash(url, 8))

    if url_input.expiration_hrs == 0:
        link.expiration = None
    else:
        now = datetime.now()
        link.expiration = max(
            link.expiration or now,
            now + timedelta(hours=url_input.expiration_hrs)
        )

    db.add(link)
    db.commit()

    base_url = str(request.base_url).rstrip("/")
    return {"short_url": f"{base_url}/{link.hash}"}

@router.get("/{hash}")
def follow_shortlink(hash: str, db: Session = Depends(db_session_default_params)):
    link = db.query(Link).filter_by(hash=hash).first()
    if not link:
        raise HTTPException(status_code=http.client.NOT_FOUND, detail={"error": "Link not found"})

    if link.expiration and link.expiration < datetime.now():
        raise HTTPException(status_code=http.client.GONE, detail={"error": "Link expired"})

    return RedirectResponse(url=link.url)