from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.database import SessionLocal
from app.services import URLService

router = APIRouter()

url_service = URLService()

templates = Jinja2Templates(directory="templates")


def get_db():
    """
    Dependency function to get a database session.
    Yields:
        Session: SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/', response_class=HTMLResponse)
async def create_short_url(request: Request, url: str = Form(...),
                           db: Session = Depends(get_db)):
    """Create a shortened URL."""
    try:
        original_url = url
        if not original_url:
            raise HTTPException(status_code=400, detail='URL is required')
        short_id = url_service.create_short_url(original_url, db)
        short_url = f'http://127.0.0.1:8080/{short_id}'
        return templates.TemplateResponse(
            'index.html', {'request': request, 'short_url': short_url})
    except Exception:
        raise HTTPException(status_code=500, detail='Internal server error')


@router.get('/{short_id}')
async def get_original_url(short_id: str, db: Session = Depends(get_db)):
    """Redirect to the original URL."""
    try:
        original_url = url_service.get_original_url(short_id, db)
        if not original_url:
            raise HTTPException(status_code=404, detail='URL not found')
        return RedirectResponse(url=original_url, status_code=307)
    except Exception:
        raise HTTPException(status_code=500, detail='Internal server error')
