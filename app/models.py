from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from src.database import Base
from pydantic import BaseModel, HttpUrl


class UrlOrm(Base):
    """
    ORM model for storing URL addresses.
    Attributes:
        id (int): Primary key of the record.
        original_url (str): Original URL.
        short_url (str): Shortened URL.
    """
    __tablename__ = 'urls'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    original_url: Mapped[str] = mapped_column(String, nullable=False)
    short_url: Mapped[str] = mapped_column(String, nullable=False)


class URLCreate(BaseModel):
    """
    Pydantic model for creating a shortened URL.

    Attributes:
        url (HttpUrl): The original URL to be shortened.
        Must be a valid HTTP or HTTPS URL.
    """
    url: HttpUrl
