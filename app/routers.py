from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import URLService
from app.models import URLCreate
from src.database import get_async_session


router = APIRouter()

templates = Jinja2Templates(directory='templates')


@router.post('/', response_class=HTMLResponse)
async def create_short_url(
    request: Request,
    url: str = Form(...),
    db: AsyncSession = Depends(get_async_session),
):
    """Create a shortened URL."""
    try:
        url_service = URLService(db)
        url_data = URLCreate(url=url)
        short_id = await url_service.create_short_url(url_data.url)
        short_url = f'http://127.0.0.1:8080/{short_id}'
        return templates.TemplateResponse(
            'index.html', {'request': request, 'short_url': short_url})
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Internal server error')


@router.get('/{short_id}')
async def get_original_url(
    short_id: str,
    db: AsyncSession = Depends(get_async_session)
):
    """Redirect to the original URL."""
    try:
        url_service = URLService(db)
        original_url = await url_service.get_original_url(short_id)
        if not original_url:
            raise HTTPException(status_code=404, detail='URL not found')
        return RedirectResponse(url=original_url, status_code=307)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Internal server error')
