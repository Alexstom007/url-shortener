import hashlib

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import UrlOrm


class URLService:
    """Service for URL shortening operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    def generate_short_id(self, url: str) -> str:
        """Generate a short ID for the URL using MD5 hash."""
        return hashlib.md5(url.encode()).hexdigest()[:8]

    async def create_short_url(self, original_url: str) -> str:
        """Create a shortened URL."""
        original_url_str = str(original_url)
        result = await self.db.execute(select(UrlOrm).where(
            UrlOrm.original_url == original_url_str))
        db_url = result.scalar_one_or_none()
        if db_url:
            return db_url.short_url
        short_id = self.generate_short_id(original_url_str)
        new_url = UrlOrm(original_url=original_url_str, short_url=short_id)
        self.db.add(new_url)
        await self.db.commit()
        await self.db.refresh(new_url)
        return short_id

    async def get_original_url(self, short_id: str) -> str:
        """Get original URL by short ID."""
        result = await self.db.execute(select(UrlOrm).where(
            UrlOrm.short_url == short_id))
        db_url = result.scalar_one_or_none()
        if not db_url:
            raise HTTPException(status_code=404, detail='URL not found')
        return db_url.original_url
