from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Comment, Recipe

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def require_nonblank(value: str, field_name: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise HTTPException(status_code=422, detail=f"{field_name} cannot be blank")
    return cleaned

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@router.get("/browse", response_class=HTMLResponse)
async def browse(
    request: Request,
    search: str = "",
    author: str = "",
    tag: str = "",
    db: Session = Depends(get_db),
):
    query = db.query(Recipe)

    if search:
        keyword = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Recipe.title.ilike(keyword),
                Recipe.description.ilike(keyword),
                Recipe.ingredients.ilike(keyword),
            )
        )

    if author:
        query = query.filter(Recipe.author.ilike(f"%{author.strip()}%"))

    if tag:
        query = query.filter(Recipe.tags.ilike(f"%{tag.strip()}%"))

    recipes = query.order_by(Recipe.created_at.desc(), Recipe.id.desc()).all()
    return templates.TemplateResponse(
        request=request,
        name="browse.html",
        context={
            "recipes": recipes,
            "filters": {"search": search, "author": author, "tag": tag},
        },
    )

@router.get("/add", response_class=HTMLResponse)
async def add_recipe(request: Request):
    return templates.TemplateResponse(request=request, name="add.html")

@router.post("/add")
async def create_recipe(
    title: Annotated[str, Form(min_length=1, max_length=120)],
    author: Annotated[str, Form(min_length=1, max_length=80)],
    description: Annotated[str, Form(max_length=500)] = "",
    ingredients: Annotated[str, Form(min_length=1, max_length=4000)] = "",
    steps: Annotated[str, Form(min_length=1, max_length=6000)] = "",
    tags: Annotated[str, Form(max_length=200)] = "",
    db: Session = Depends(get_db),
):
    recipe = Recipe(
        title=require_nonblank(title, "Title"),
        author=require_nonblank(author, "Author"),
        description=description.strip(),
        ingredients=require_nonblank(ingredients, "Ingredients"),
        steps=require_nonblank(steps, "Steps"),
        tags=tags.strip(),
    )
    db.add(recipe)
    db.commit()

    return RedirectResponse(url="/browse", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/recipes/{id}", response_class=HTMLResponse)
async def recipe_detail(request: Request, id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
        
    return templates.TemplateResponse(request=request, name="detail.html", context={"recipe": recipe})

@router.post("/recipes/{id}/comments")
async def create_comment(
    id: int,
    name: Annotated[str, Form(min_length=1, max_length=80)],
    comment_text: Annotated[str, Form(min_length=1, max_length=1000)],
    db: Session = Depends(get_db),
):
    recipe = db.query(Recipe).filter(Recipe.id == id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    comment = Comment(
        recipe_id=recipe.id,
        name=require_nonblank(name, "Name"),
        comment_text=require_nonblank(comment_text, "Comment"),
    )
    db.add(comment)
    db.commit()

    return RedirectResponse(
        url=f"/recipes/{recipe.id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )

@router.post("/recipes/{id}/delete")
async def delete_recipe(id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
        
    db.delete(recipe)
    db.commit()
    return RedirectResponse(url="/browse", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(request=request, name="about.html")
