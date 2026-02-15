## Technology Stack

### Backend
* **Runtime:** Python 3.12
* **Framework:** FastAPI
* **Web Server:** Uvicorn (ASGI server)
* **Database:** *[TBD - SQLite hosted by EC2?]*

### Frontend
* **Templates/UI:** *[TBD]*
* **Styling:** *[TBD]*

### Testing & DevOps
* **Testing Framework:** pytest
* **CI/CD:** GitHub Actions

---

## Team Workflow

**Team Members:** amdrao9121, christopherhasti

### Workflow Strategy: Single Repository with Collaborators
We have adopted a collaborative feature-branch workflow to ensure code quality and stability in the `main` branch.

1. **Access Control:**
   * Both team members have Write access to the repository.
   * Direct commits to the `main` branch are restricted; all changes must pass through a Pull Request (PR).

2. **Branching Convention:**
   * Development work is done on isolated branches created for specific tasks.
   * **Naming convention:** `category/description` (e.g., `feature/auth-login`, `fix/ci-pipeline`, `docs/update-readme`).

3. **Merge Requirements:**
   * **Pull Requests:** When a feature is complete, a Pull Request is opened against `main`.
   * **Continuous Integration:** Merging is blocked until the CI pipeline (running `pytest`) passes successfully.
   * **Code Review:** At least one review/approval from a teammate is required before merging.