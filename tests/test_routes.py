from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "RecipeShare" in response.text

def test_browse_page():
    response = client.get("/browse")
    assert response.status_code == 200
    assert "All <em>Recipes</em>" in response.text

def test_add_page():
    response = client.get("/add")
    assert response.status_code == 200
    assert "Share a <em>Recipe</em>" in response.text

def test_recipe_detail_page():
    # Testing with a placeholder ID of 1
    response = client.get("/recipes/1")
    assert response.status_code == 200
    assert "[Recipe Title Placeholder]" in response.text

def test_about_page():
    response = client.get("/about")
    assert response.status_code == 200
    assert "The Developers" in response.text