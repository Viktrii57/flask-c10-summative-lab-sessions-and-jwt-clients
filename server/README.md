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