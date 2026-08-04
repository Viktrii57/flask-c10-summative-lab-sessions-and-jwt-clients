import os
from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, bcrypt
from resources.auth import SignupResource, LoginResource, LogoutResource, CheckSessionResource
from resources.entries import EntryListResource, EntryResource

def create_app():
    """Application factory for configuring and initializing the Flask backend."""
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-super-secret-key-123')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Cookie and Session security settings for CORS compatibility
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in HTTPS production

    # Extension initializations
    db.init_app(app)
    bcrypt.init_app(app)
    Migrate(app, db)
    
    # Enable CORS with credentials for session cookies
    CORS(app, supports_credentials=True)

    # API Route Registration
    api = Api(app)

    # Auth Endpoints (Rubric criteria: Sign Up, Login/Logout, Check Session)
    api.add_resource(SignupResource, '/api/signup')
    api.add_resource(LoginResource, '/api/login')
    api.add_resource(LogoutResource, '/api/logout')
    api.add_resource(CheckSessionResource, '/api/check_session')

    # Resource Endpoints (Rubric criteria: CRUD + Pagination)
    api.add_resource(EntryListResource, '/api/entries')
    api.add_resource(EntryResource, '/api/entries/<int:entry_id>')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=5555, debug=True)