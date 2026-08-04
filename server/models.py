from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    """User model with secure password hashing and uniqueness constraints."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Cascade deletes to clean up child resources on user deletion
    entries = db.relationship('JournalEntry', backref='owner', lazy=True, cascade='all, delete-orphan')

    @property
    def password(self):
        raise AttributeError('Password is a write-only attribute.')

    @password.setter
    def password(self, plain_text_password):
        """Hashes raw password before storing in database."""
        self._password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password(self, plain_text_password):
        """Verifies plain text password against stored hash."""
        return bcrypt.check_password_hash(self._password_hash, plain_text_password)


class JournalEntry(db.Model):
    """User-owned Journal Entry resource model with custom fields."""
    __tablename__ = 'journal_entries'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default='General')  # field 1
    mood_score = db.Column(db.Integer, default=5)          # field 2
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Explicit Foreign Key relationship establishing ownership
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)