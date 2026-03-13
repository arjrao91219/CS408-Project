from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Set up the templates directory
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/browse", response_class=HTMLResponse)
async def browse(request: Request):
    return templates.TemplateResponse("browse.html", {"request": request})

@app.get("/add", response_class=HTMLResponse)
async def add_recipe(request: Request):
    return templates.TemplateResponse("add.html", {"request": request})

@app.get("/recipes/{id}", response_class=HTMLResponse)
async def recipe_detail(request: Request, id: int):
    # Conditionally retrieves based on recipe ID in the future
    return templates.TemplateResponse("detail.html", {"request": request, "id": id})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})