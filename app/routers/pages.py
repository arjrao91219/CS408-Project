from fastapi import APIRouter, Depends, Form, Request, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Comment, Recipe

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

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
    title: str = Form(...),
    author: str = Form(...),
    description: str = Form(""),
    ingredients: str = Form(...),
    steps: str = Form(...),
    tags: str = Form(""),
    db: Session = Depends(get_db),
):
    recipe = Recipe(
        title=title.strip(),
        author=author.strip(),
        description=description.strip(),
        ingredients=ingredients.strip(),
        steps=steps.strip(),
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
    name: str = Form(...),
    comment_text: str = Form(...),
    db: Session = Depends(get_db),
):
    recipe = db.query(Recipe).filter(Recipe.id == id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    comment = Comment(
        recipe_id=recipe.id,
        name=name.strip(),
        comment_text=comment_text.strip(),
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
