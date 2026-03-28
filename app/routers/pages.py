from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@router.get("/browse", response_class=HTMLResponse)
async def browse(request: Request):
    return templates.TemplateResponse(request=request, name="browse.html")

@router.get("/add", response_class=HTMLResponse)
async def add_recipe(request: Request):
    return templates.TemplateResponse(request=request, name="add.html")

@router.get("/recipes/{id}", response_class=HTMLResponse)
async def recipe_detail(request: Request, id: int):
    # Conditionally retrieves based on recipe ID in the future
    return templates.TemplateResponse(request=request, name="detail.html", context={"id": id})

@router.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(request=request, name="about.html")