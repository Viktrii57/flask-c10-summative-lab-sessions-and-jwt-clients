# Full Auth Flask Backend - Productivity Journal API

A RESTful Flask API backend delivering full user authentication, session-based route protection, user-scoped data access controls, and pagination for personal productivity tracking.

## Features
- **User Authentication**: Sign Up, Login, Logout, and Session Check (`/api/check_session`).
- **Data Protection**: Bcrypt password hashing and user isolation for entries.
- **Resource Management**: CRUD operations on `JournalEntry` with custom fields (`category`, `mood_score`).
- **Pagination**: Paginated index endpoint for scalable data delivery.

## Installation Instructions

1. **Navigate to the server directory:**

   ```bash
   cd server

2. **Install dependancies via pipenv:**

   bash
   pipenv install
   pipenv shell

3. **Initialize and seed the SQLite database:**

   bash
   flask db init
   flask db migrate -m "Initial schema setup"
   flask db upgrade
   python seed.py

## Run Instructions

1. **Start the development server:**

   bash
   python app.py

   **API Base URL: http://127.0.0.1:5555**


### Git Workflow 

**Git Workflow & Management** 

```bash
# 1. Create a feature branch
git checkout -b feature/auth-and-crud

# 2. Stage and commit regularly with clear messages
git add server/
git commit -m "feat: setup Flask app factory, models, and bcrypt hashing"

git commit -m "feat: implement session auth endpoints and check_session route"

git commit -m "feat: implement user-isolated resource CRUD and pagination"

# 3. Push and merge back to main
git checkout main
git merge feature/auth-and-crud
git push origin main