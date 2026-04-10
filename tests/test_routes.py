import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import Recipe

@pytest.fixture
def client(tmp_path):
    db_path = tmp_path / "test_recipes.db"
    engine = create_engine(
        f"sqlite:///{db_path}", connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        test_client.testing_session_factory = TestingSessionLocal
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "RecipeShare" in response.text

def test_browse_page(client):
    response = client.get("/browse")
    assert response.status_code == 200
    assert "All <em>Recipes</em>" in response.text

def test_add_page(client):
    response = client.get("/add")
    assert response.status_code == 200
    assert "Share a <em>Recipe</em>" in response.text

def test_create_recipe(client):
    response = client.post(
        "/add",
        data={
            "title": "Spicy Peanut Noodles",
            "author": "Ahmad",
            "description": "A quick weeknight noodle bowl.",
            "ingredients": "Noodles\nPeanut butter\nSoy sauce",
            "steps": "Boil noodles\nWhisk sauce\nCombine",
            "tags": "quick, noodles, vegetarian",
        },
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers["location"] == "/browse"

    db = client.testing_session_factory()
    try:
        recipes = db.query(Recipe).all()
        assert len(recipes) == 1
        assert recipes[0].title == "Spicy Peanut Noodles"
        assert recipes[0].author == "Ahmad"
    finally:
        db.close()

def test_recipe_detail_page(client):
    # First inject a recipe
    db = client.testing_session_factory()
    try:
        recipe = Recipe(
            title="Detail Test Recipe",
            author="Chris",
            description="Testing DB fetch",
            ingredients="Ing 1\nIng 2",
            steps="Step 1",
        )
        db.add(recipe)
        db.commit()
        db.refresh(recipe)
        recipe_id = recipe.id
    finally:
        db.close()

    # Now conditionally retrieve
    response = client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    assert "Detail Test Recipe" in response.text
    assert "Testing DB fetch" in response.text
    assert "Chris" in response.text

def test_recipe_detail_404(client):
    # Access an ID that does not exist
    response = client.get("/recipes/999")
    assert response.status_code == 404
    assert "Recipe Not Found" in response.text

def test_delete_recipe(client):
    # Inject a recipe
    db = client.testing_session_factory()
    try:
        recipe = Recipe(
            title="Delete Me",
            author="Ahmad",
            ingredients="Air",
            steps="Delete",
        )
        db.add(recipe)
        db.commit()
        db.refresh(recipe)
        recipe_id = recipe.id
    finally:
        db.close()

    # Fire POST Delete Request
    response = client.post(f"/recipes/{recipe_id}/delete", follow_redirects=False)
    
    # Should redirect to browse
    assert response.status_code == 303
    assert response.headers["location"] == "/browse"

    # Confirm it's missing from DB
    db = client.testing_session_factory()
    try:
        recipe_check = db.query(Recipe).filter(Recipe.id == recipe_id).first()
        assert recipe_check is None
    finally:
        db.close()

def test_about_page(client):
    response = client.get("/about")
    assert response.status_code == 200
    assert "The Developers" in response.text