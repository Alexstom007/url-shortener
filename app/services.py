import hashlib
from typing import Dict
from urllib.parse import urlparse

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import UrlOrm


class URLService:
    """Service for URL shortening operations."""

    def __init__(self):
        self.url_storage: Dict[str, str] = {}

    def validate_url(self, url: str) -> None:
        """Validate URL format and scheme."""
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                raise HTTPException(
                    status_code=400,
                    detail='Invalid URL format. URL must include scheme'
                           '(http/https) and domain'
                )
            if parsed.scheme not in ['http', 'https']:
                raise HTTPException(
                    status_code=400,
                    detail='Only http and https URLs are supported'
                )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f'Invalid URL: {str(e)}'
            )

    def generate_short_id(self, url: str) -> str:
        """Generate a short ID for the URL using MD5 hash."""
        return hashlib.md5(url.encode()).hexdigest()[:8]

    def create_short_url(self, original_url: str, db: Session) -> str:
        """Create a shortened URL."""
        self.validate_url(original_url)
        db_url = db.query(
            UrlOrm).filter(UrlOrm.original_url == original_url).first()
        if db_url:
            return db_url.short_url
        short_id = self.generate_short_id(original_url)
        new_url = UrlOrm(original_url=original_url, short_url=short_id)
        db.add(new_url)
        db.commit()
        db.refresh(new_url)
        return short_id

    def get_original_url(self, short_id: str, db: Session) -> str:
        """Get original URL by short ID."""
        db_url = db.query(UrlOrm).filter(UrlOrm.short_url == short_id).first()
        if not db_url:
            raise HTTPException(status_code=404, detail="URL not found")
        return db_url.original_url
