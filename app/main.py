from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from app.routers import pages

# Create database tables locally on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="RecipeShare API")

# Mount static assets
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include the UI router
app.include_router(pages.router)