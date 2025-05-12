import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.routers import router
from src.database import Base, engine


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app = FastAPI(title='URL Shortener Service')
app.include_router(router)

templates = Jinja2Templates(directory='templates')


@app.on_event("startup")
async def startup_event():
    await init_db()


@app.get('/', response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8080)
