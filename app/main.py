from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.database import engine, Base
from app.routers import pages

# Create database tables locally on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="RecipeShare API")

# Mount static assets
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

# Custom 404 Exception Handler
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse(request=request, name="404.html", status_code=404)
    # Fallback for other errors
    return templates.TemplateResponse(request=request, name="404.html", status_code=exc.status_code)

# Include the UI router
app.include_router(pages.router)