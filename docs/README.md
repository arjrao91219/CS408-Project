## RecipeShare

Collaborative Recipe Sharing Platform for CS 408.

### Stack

- Python 3.12+
- FastAPI
- Jinja2 templates
- SQLAlchemy
- SQLite for local development
- PostgreSQL for EC2 deployment
- Pytest

### Project Layout

- `app/main.py`: FastAPI app setup and error handling
- `app/database.py`: database configuration and session management
- `app/models.py`: SQLAlchemy models for recipes and comments
- `app/routers/pages.py`: page routes, create/list/detail/delete/comment flows
- `app/templates/`: Jinja templates
- `scripts/setup_ec2.sh`: base EC2 system setup
- `scripts/configure_app.sh`: app, service, and Nginx configuration
- `tests/`: route and smoke tests

### Local Setup

From the project root:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run Locally

Start the app with:

```bash
uvicorn app.main:app --reload
```

Open:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/browse`
- `http://127.0.0.1:8000/add`

### Local Database

Local development uses SQLite by default:

- file: `recipes.db`

No extra setup is required. Tables are created automatically on app startup.

### Environment Variables

Optional environment variables:

```bash
DATABASE_URL=postgresql://user:password@host/dbname
PORT=8000
```

If `DATABASE_URL` is not set, the app falls back to local SQLite.

### Run Tests

Run the full test suite with:

```bash
pytest
```

The tests use an isolated temporary SQLite database and do not depend on your local `recipes.db` contents.

### Features Implemented

- Home, Browse, Add Recipe, Detail, About pages
- Shared layout with navigation and footer
- Create recipe
- List and filter recipes
- View a recipe by ID
- Delete recipes from browse and detail pages
- Add and display recipe comments
- Custom 404 page for missing recipes

### Deployment on EC2

The repository includes two deployment scripts:

- `scripts/setup_ec2.sh`
  - installs Python, PostgreSQL, and Nginx
  - creates the PostgreSQL user and database
- `scripts/configure_app.sh`
  - creates a virtual environment
  - installs dependencies
  - writes the `.env`
  - initializes database tables
  - configures Gunicorn + Uvicorn systemd service
  - configures Nginx reverse proxy

Typical deployment flow:

```bash
sudo bash scripts/setup_ec2.sh
bash scripts/configure_app.sh
```

### Notes

- User input is server-side constrained with basic length validation.
- Jinja autoescaping is used for template rendering.
- Comments are tied to a specific recipe through a foreign key relationship.
